from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Editor_Review
from .forms import Editors_Reviews_Form
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from users.models import Editor
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from core.models import NoQuerySet, AuthorNotMatched
from django.core.files.uploadedfile import SimpleUploadedFile
from config.settings import BASE_DIR
import os
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from comments.forms import EditorReviewCommentForm, EditorReviewRecommentForm
from comments.models import Editor_Review_Comment, Editor_Review_Recomment
from django.http import JsonResponse, HttpResponse
from users.models import User


def index(request):
    try:
        first_review = Editor_Review.objects.first()
        if first_review is None:
            raise NoQuerySet
        review_list = Editor_Review.objects.all()[1:]
        if review_list is None:
            raise NoQuerySet
        editors = Editor.objects.all()
        if editors is None:
            raise NoQuerySet
        ctx = {
            "first_review": first_review,
            "review_list": review_list,
            "editors": editors,
        }
        return render(request, "editor_reviews/editor_reviews_list.html", ctx)
    except NoQuerySet:
        return redirect(reverse("core:main"))


def detail(request, pk):
    review = get_object_or_404(Editor_Review, pk=pk)
    ctx = {
        "review": review,
    }
    return render(request, "editor_reviews/editor_reviews_detail.html", ctx)


class Editor_review_detail(DetailView):
    model = Editor_Review
    template_name = "editor_reviews/detail/editor_reviews_detail.html"
    context_object_name = "review"
    # form_class = EditorReviewCommentForm

    # def get_success_url(self):
    #     return reverse('editor_reviews:detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        ctx = super(DetailView, self).get_context_data(**kwargs)
        comments = Editor_Review_Comment.objects.filter(editor_review=self.get_object())

        ctx["comments"] = comments.order_by("-create_at")[: min(10, len(comments))]
        ctx["form"] = EditorReviewCommentForm()

        if self.request.user != AnonymousUser():
            ctx["user"] = self.request.user

        else:
            ctx["user"] = None

        return ctx

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)

        try:
            if self.request.user == AnonymousUser():
                raise ObjectDoesNotExist

            user = Editor.objects.get(user=self.request.user)

            if self.get_object().author == user:
                new_comments = Editor_Review_Comment.objects.filter(
                    editor_review=self.get_object(), is_read=False
                )

                for comment in new_comments:
                    comment.is_read = True
                    comment.save()

        except ObjectDoesNotExist:
            pass

        if self.request.session.get("_auth_user_id") is None:
            cookie_name = "editor_review_hit"

        else:
            cookie_name = f'editor_review_hit:{self.request.session["_auth_user_id"]}'

        if self.request.COOKIES.get(cookie_name) is None:
            response.set_cookie(cookie_name, self.kwargs["pk"], 3600)

            review = self.get_object()
            review.hits += 1
            review.save()

        else:
            cookie = self.request.COOKIES.get(cookie_name)
            cookies = cookie.split("|")

            if str(self.kwargs["pk"]) not in cookies:
                response.set_cookie(cookie_name, cookie + f'|{self.kwargs["pk"]}', 3600)

                review = self.get_object()
                review.hits += 1
                review.save()

        return response

    # def post(self, request, pk):
    #     self.object = self.get_object()
    #     form = self.get_form()

    #     if form.is_valid():
    #         return self.form_valid(form)

    #     else:
    #         return self.form_invalid(form)

    # def form_valid(self, form):
    #     comment = form.save(commit=False)
    #     comment.editor_review = get_object_or_404(Editor_Review, pk=self.object.pk)
    #     comment.author = self.request.user
    #     comment.save()
    #     return super().form_valid(form)


def editor_review_comment(request, pk):
    post = get_object_or_404(Editor_Review, pk=pk)
    author = request.user
    text = request.POST.get("text")

    comment = Editor_Review_Comment(editor_review=post, author=author, text=text)
    comment.save()

    data = {
        "text": text,
        "create_at": comment.create_at.strftime(
            r"%Y. %m. %d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%H : %M"
        ),
        "author": author.nickname,
        "profile_image": author.profile_image.url,
        "pk": comment.id,
    }

    return JsonResponse(data)


def editor_review_comment_load(request):
    """Editor's Pick 댓글 불러오기 - AJAX"""

    # AJAX 요청인 경우에만 실행 한다.
    if request.is_ajax():
        current_comment_count = int(
            request.POST.get("numberOfComments")
        )  # Front-end 에서 현재 로딩된 댓글의 개수를 요청에 포함한다.
        pk = request.POST.get("pk")
        review = Editor_Review.objects.get(pk=pk)
        comments = Editor_Review_Comment.objects.filter(editor_review=review).order_by(
            "-create_at"
        )

        try:
            # Posting의 전체 댓글 중에서 아직 불러오지 않은 것들을 가져온다. (10개 혹은 그 이하)
            unloaded_comments = comments[
                current_comment_count : min(
                    current_comment_count + 10, comments.count()
                )
            ]

            # Front-end에서 동적으로 엘리먼트를 생성할 때 사용 가능한 방식으로 데이터를 분리한다.
            comment_list = list(
                map(
                    lambda u: {
                        "author": u.author.nickname,
                        "profile_image": u.author.profile_image.url,
                        "text": u.text,
                        "create_at": u.create_at.strftime(
                            r"%Y. %m. %d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%H : %M"
                        ),
                        "like_count": u.like_count(),
                        "pk": u.id,
                    },
                    unloaded_comments,
                )
            )

            ctx = {"comment_list": comment_list}

            return JsonResponse(ctx)

        except ObjectDoesNotExist:
            # 더 이상 불러올 댓글이 없으면 HTTP 204 (No Content)를 리턴한다.
            return HttpResponse("이미 모든 댓글을 불러왔습니다.", status=204)

    # AJAX에 의한 접근이 아닌 경우 HTTP 400 (Bad Request)를 리턴한다.
    return HttpResponse("잘못된 접근입니다.", status=400)


def editor_review_comment_delete(request, reviewpk, commentpk):
    # editor's pick 댓글 삭제 - AJAX

    if request.is_ajax():
        comment = get_object_or_404(Editor_Review_Comment, pk=commentpk)

        ctx = {"status": True}

        comment.delete()

    return JsonResponse(ctx)


def editor_review_comment_edit(request, reviewpk, commentpk):
    """Editor's pick 댓글 수정 - AJAX"""
    if request.is_ajax():
        comment = Editor_Review_Comment.objects.get(pk=commentpk)
        text = request.POST.get("text")

        comment.text = text
        comment.save()

        ctx = {
            "update_at": comment.updated_at.strftime(
                r"%Y. %m. %d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%H : %M"
            ),
            "status": True,
        }

        return JsonResponse(ctx)


def editor_review_recomment(request, reviewpk, commentpk):
    comment = get_object_or_404(Editor_Review_Comment, pk=commentpk)
    author = request.user
    text = request.POST.get("text")

    recomment = Editor_Review_Recomment(comment=comment, author=author, text=text)
    recomment.save()

    data = {
        "text": text,
        "create_at": comment.create_at.strftime(
            r"%Y. %m. %d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%H : %M"
        ),
        "author": author.nickname,
        "profile_image": author.profile_image.url,
        "pk": recomment.pk,
    }

    return JsonResponse(data)


def editor_review_recomment_edit(request):
    pk = request.POST.get("pk")
    text = request.POST.get("text")

    comment = get_object_or_404(Editor_Review_Recomment, pk=pk)
    comment.text = text
    comment.save()

    ctx = {
        "update_at": comment.updated_at.strftime(
            r"%Y. %m. %d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%H : %M"
        ),
        "status": True,
    }

    return JsonResponse(ctx)


def editor_review_recomment_delete(request):
    pk = request.POST.get("pk")
    print(pk)

    comment = get_object_or_404(Editor_Review_Recomment, pk=pk)
    comment.delete()

    ctx = {
        "status": True,
    }

    return JsonResponse(ctx)


@login_required
def create(request):
    try:
        user = request.user.editor
    except ObjectDoesNotExist:
        return redirect(reverse("editors_pick:index"))

    if request.method == "POST":
        form = Editors_Reviews_Form(request.POST, request.FILES)
        if form.is_valid():
            print("form validation 완료")
            post_category = form.cleaned_data.get("post_category")
            title = form.cleaned_data.get("title")
            sub_title = form.cleaned_data.get("sub_title")
            main_image = form.cleaned_data.get("main_image")
            contents = form.cleaned_data.get("contents")
            farm = form.cleaned_data.get("farm")
            print(farm)
            editor_review = Editor_Review(
                post_category=post_category,
                title=title,
                sub_title=sub_title,
                main_image=main_image,
                contents=contents,
                farm=farm,
            )
            editor_review.author = user
            editor_review.save()
            editor_review.product.set(form.cleaned_data.get("product"))
            editor_review.save()
            return redirect(reverse("editors_pick:detail", args=[editor_review.pk]))
        else:
            print("form validation 실패")
            return redirect(reverse("core:main"))
    else:
        form = Editors_Reviews_Form()
        ctx = {
            "form": form,
        }
        return render(request, "editor_reviews/editor_reviews_create.html", ctx)


@login_required
def update(request, pk):
    post = get_object_or_404(Editor_Review, pk=pk)

    try:
        user = request.user.editor
        if post.author != user:
            raise AuthorNotMatched
    except ObjectDoesNotExist:
        return redirect(reverse("core:main"))
    except AuthorNotMatched:
        return redirect(reverse("core:main"))

    if request.method == "POST":
        form = Editors_Reviews_Form(request.POST, request.FILES)
        if form.is_valid():
            print("form validation 완료")
            post.title = form.cleaned_data["title"]
            post.main_image = form.cleaned_data["main_image"]
            post.contents = form.cleaned_data["contents"]
            post.product = form.cleaned_data["product"]
            post.updated_at = timezone.now()
            post.save()
            return redirect("editors_pick:detail", pk)
        else:
            print("form validation 실패")
            return redirect(reverse("core:main"))
    else:
        # form_data = {
        #     'title': post.title,
        #     'contents': post.contents,
        #     'post_category': post.post_category,
        #     'product_category': post.product_category,
        #     'product': post.product,
        # }
        # main_image_path = os.path.join(BASE_DIR, post.main_image)
        # print(main_image_path)
        # with open(main_image_path, 'rb') as f:
        #     image_data = {
        #         'main_image': SimpleUploadedFile('sumbnail', f.read()),
        #     }
        form = Editors_Reviews_Form(instance=post)

        ctx = {
            "post": post,
            "form": form,
        }
        return render(request, "editor_reviews/editor_reviews_update.html", ctx)


@login_required
def delete(request):
    if not request.is_ajax():
        return redirect(reverse("core:main"))

    reviewpks = request.POST.getlist("select[]")

    for reviewpk in reviewpks:
        review = Editor_Review.objects.get(pk=reviewpk)
        review.delete()

    ctx = {
        "success": True,
    }

    return JsonResponse(ctx)

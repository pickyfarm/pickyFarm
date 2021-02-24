from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Editor_Review
from .forms import Editors_Reviews_Form
from django.views.generic import DetailView
from users.models import Editor
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from core.models import NoQuerySet, AuthorNotMatched
from django.core.files.uploadedfile import SimpleUploadedFile
from config.settings import BASE_DIR
import os
from django.utils import timezone


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
            'first_review': first_review,
            'review_list': review_list,
            'editors': editors,
        }
        return render(request, 'editor_reviews/editor_reviews_list.html', ctx)
    except NoQuerySet:
        return redirect(reverse('core:main'))


def detail(request, pk):
    review = get_object_or_404(Editor_Review, pk=pk)
    ctx = {
        'review': review,
    }
    return render(request, 'editor_reviews/editor_reviews_detail.html', ctx)

class Editor_review_detail(DetailView):
    model = Editor_Review
    template_name = "editor_reviews/editor_reviews_detail.html"
    context_object_name = "review"
    
    def get_context_data(self, **kwargs):
        ctx = super(DetailView, self).get_context_data(**kwargs)
        ctx['comments'] = self.get_object().editor_review_comments.all()

        return ctx

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)

        if self.request.session.get('_auth_user_id') is None:
            cookie_name = 'editor_review_hit'
        
        else:
            cookie_name = f'editor_review_hit:{self.request.session["_auth_user_id"]}'

        
        if self.request.COOKIES.get(cookie_name) is None:
            response.set_cookie(cookie_name, self.kwargs['pk'], 3600)

            review = self.get_object()
            review.hits += 1
            review.save()

        else:
            cookie = self.request.COOKIES.get(cookie_name)
            cookies = cookie.split('|')

            if str(self.kwargs['pk']) not in cookies:
                response.set_cookie(cookie_name, cookie + f'|{self.kwargs["pk"]}', 3600)
                
                review = self.get_object()
                review.hits += 1
                review.save()


        return response



@login_required
def create(request):
    try:
        user = request.user.editor
    except ObjectDoesNotExist:
        return redirect(reverse('editors_pick:index'))

    if request.method == 'POST':
        form = Editors_Reviews_Form(request.POST, request.FILES)
        if form.is_valid():
            print("form validation 완료")
            post_category = form.cleaned_data.get('post_category')
            title = form.cleaned_data.get('title')
            sub_title = form.cleaned_data.get('sub_title')
            main_image = form.cleaned_data.get('main_image')
            contents = form.cleaned_data.get('contents')
            farm = form.cleaned_data.get('farm')
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
            editor_review.product.set(form.cleaned_data.get('product'))
            editor_review.save()
            return redirect(reverse('editors_pick:detail', args=[editor_review.pk]))
        else:
            print("form validation 실패")
            return redirect(reverse("core:main"))
    else:
        form = Editors_Reviews_Form()
        ctx = {
            'form': form,
        }
        return render(request, 'editor_reviews/editor_reviews_create.html', ctx)


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

    if request.method == 'POST':
        form = Editors_Reviews_Form(request.POST, request.FILES)
        if form.is_valid():
            print("form validation 완료")
            post.title = form.cleaned_data['title']
            post.main_image = form.cleaned_data['main_image']
            post.contents = form.cleaned_data['contents']
            post.product = form.cleaned_data['product']
            post.updated_at = timezone.now()
            post.save()
            return redirect('editors_pick:detail', pk)
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
            'post': post,
            'form': form,
        }
        return render(request, 'editor_reviews/editor_reviews_update.html', ctx)


@login_required
def delete(request, pk):
    post = get_object_or_404(Editor_Review, pk=pk)

    try:
        user = request.user.editor
        if post.author != user:
            raise AuthorNotMatched
    except ObjectDoesNotExist:
        return redirect(reverse("core:main"))
    except AuthorNotMatched:
        return redirect(reverse("core:main"))

    post.delete()

    return redirect(reverse('core:main'))

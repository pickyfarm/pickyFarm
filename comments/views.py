from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import (
    Product_Comment,
    Product_Comment_Image,
    Product_Recomment,
    Farmer_Story_Comment,
    Farmer_Story_Recomment,
)
from .forms import ProductCommentForm, ProductRecommentForm
from products.models import Product
from users.models import Consumer
from farmers.models import Farmer_Story
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


"""
product comments(reviews)
"""


def product_comment_detail(request, pk):
    """Product 댓글 보기"""
    product = Product.objects.get(pk=pk)
    product_comments = product.product_comments.all()
    product_comment_form = ProductCommentForm()
    product_recomment_form = ProductRecommentForm()

    ctx = {
        "product": product,
        "product_comments": product_comments,
        "product_comment_form": product_comment_form,
        "product_recomment_form": product_recomment_form,
    }

    return render(request, "comments/product_comment.html", ctx)


def product_comment_update(request, pk):
    """Product 댓글 수정"""

    product_comment = Product_Comment.objects.get(pk=pk)
    product = product_comment.product

    if request.method == "POST":
        product_comment_form = ProductCommentForm(
            request.POST, request.FIELS, instance=product_comment
        )
        if product_comment_form.is_valid():
            product_comment = product_comment_form.save(commit=False)
            product_comment.author = request.user
            product_comment.product = product
            return redirect(reverse("comments:product_comment_detail", kwargs={"pk": pk}))
    else:
        product_comment_form = ProductCommentForm(instance=product_comment)

    return render(
        request, "comments/product_comment.html", {"product_comment_form": product_comment_form}
    )


def product_comment_delete(request, pk):
    """Product 댓글 삭제"""
    product_comment = Product_Comment.objects.get(pk=pk)
    product = product_comment.product

    if request.method == "POST":
        product_comment.delete()
        return redirect(product)
    else:
        return render(request, "coments/product_comment.html")


"""
product recomments
"""


def product_recomment_detail(request, pk):
    """Product 대댓글 보기"""
    product_comment = Product_Comment.objects.get(pk=pk)
    product = product_comment.product
    product_recomment_form = ProductRecommentForm()

    ctx = {
        "product_comment": product_comment,
        "product": product,
        "product_recomment_form": product_recomment_form,
    }

    return render(request, "comments/product_comment.html", ctx)


def product_recomment(request, productpk, commentpk):
    """Product 대댓글 작성 - AJAX"""

    comment = get_object_or_404(Product_Comment, pk=commentpk)
    author = request.user
    text = request.POST.get("text")

    recomment = Product_Recomment(comment=comment, author=author, text=text)
    recomment.save()

    data = {
        "text": text,
        "create_at": recomment.create_at.strftime(
            r"%Y. %m. %d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%H : %M"
        ),
        "author": author.nickname,
        "profile_image": author.profile_image.url,
        "pk": recomment.pk,
    }

    return JsonResponse(data)


def product_recomment_edit(request):
    """Product 대댓글 수정 - AJAX"""

    pk = request.POST.get("pk")
    text = request.POST.get("text")

    comment = get_object_or_404(Product_Recomment, pk=pk)
    comment.text = text
    comment.save()

    ctx = {
        "update_at": comment.updated_at.strftime(
            r"%Y. %m. %d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%H : %M"
        ),
        "status": True,
    }

    return JsonResponse(ctx)


def product_recomment_delete(request):
    """Product 대댓글 삭제 - AJAX"""

    pk = request.POST.get("pk")

    comment = get_object_or_404(Product_Recomment, pk=pk)
    comment.delete()

    ctx = {
        "status": True,
    }

    return JsonResponse(ctx)


"""
farmer's story comments
"""


def farmer_story_comment_load(request):
    """Farmer's story 댓글 불러오기 - AJAX"""

    if request.is_ajax():
        current_comment_count = int(request.POST.get("numberOfComments"))
        pk = request.POST.get("pk")
        review = Farmer_Story.objects.get(pk=pk)
        comments = Farmer_Story_Comment.objects.filter(story=review).order_by("-create_at")

        try:
            unloaded_comments = comments[
                current_comment_count : min(current_comment_count + 10, comments.count())
            ]

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
                        "recomment_count": u.recomment_count(),
                        "pk": u.id,
                    },
                    unloaded_comments,
                )
            )

            ctx = {"comment_list": comment_list}

            return JsonResponse(ctx)

        except ObjectDoesNotExist:
            return HttpResponse("이미 모든 댓글을 불러왔습니다.", status=204)

    return HttpResponse("잘못된 접근입니다.", status=400)


def farmer_story_comment(request, pk):
    """Farmer's story 댓글 작성 - AJAX"""
    post = get_object_or_404(Farmer_Story, pk=pk)
    author = request.user
    text = request.POST.get("text")

    comment = Farmer_Story_Comment(story=post, author=author, text=text)
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


def farmer_story_comment_edit(request, storypk, commentpk):
    """Farmer's story 댓글 수정 - AJAX"""

    if request.is_ajax():
        comment = Farmer_Story_Comment.objects.get(pk=commentpk)
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


def farmer_story_comment_delete(request, storypk, commentpk):
    """Farmer's story 댓글 삭제 - AJAX"""
    if request.is_ajax():
        comment = get_object_or_404(Farmer_Story_Comment, pk=commentpk)

        ctx = {"status": True}

        comment.delete()

    return JsonResponse(ctx)


"""
farmer's story recomments
"""


def farmer_story_recomment_load(request):
    """Farmer's story 대댓글 불러오기 - AJAX"""

    if request.is_ajax():
        current_comment_count = int(
            request.POST.get("numberOfComments")
        )  # Front-end 에서 현재 로딩된 댓글의 개수를 요청에 포함한다.
        pk = request.POST.get("pk")
        comment = Farmer_Story_Comment.objects.get(pk=pk)
        recomments = Farmer_Story_Recomment.objects.filter(comment=comment).order_by("-create_at")

        try:
            # Posting의 전체 댓글 중에서 아직 불러오지 않은 것들을 가져온다. (10개 혹은 그 이하)
            unloaded_comments = recomments[
                current_comment_count : min(current_comment_count + 5, recomments.count())
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


def farmer_story_recomment(request, storypk, commentpk):
    """Farmer's story 대댓글 작성 - AJAX"""

    comment = get_object_or_404(Farmer_Story_Comment, pk=commentpk)
    author = request.user
    text = request.POST.get("text")

    recomment = Farmer_Story_Recomment(comment=comment, author=author, text=text)
    recomment.save()

    data = {
        "text": text,
        "create_at": recomment.create_at.strftime(
            r"%Y. %m. %d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%H : %M"
        ),
        "author": author.nickname,
        "profile_image": author.profile_image.url,
        "pk": recomment.pk,
    }

    return JsonResponse(data)


# farmer's story 대댓글 update
def farmer_story_recomment_edit(request):
    """Farmer's story 대댓글 수정 - AJAX"""

    pk = request.POST.get("pk")
    text = request.POST.get("text")

    comment = get_object_or_404(Farmer_Story_Recomment, pk=pk)
    comment.text = text
    comment.save()

    ctx = {
        "update_at": comment.updated_at.strftime(
            r"%Y. %m. %d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%H : %M"
        ),
        "status": True,
    }

    return JsonResponse(ctx)


# farmer's story 대댓글 delete
def farmer_story_recomment_delete(request):
    """Farmer's story 대댓글 삭제 - AJAX"""

    pk = request.POST.get("pk")

    comment = get_object_or_404(Farmer_Story_Recomment, pk=pk)
    comment.delete()

    ctx = {
        "status": True,
    }

    return JsonResponse(ctx)

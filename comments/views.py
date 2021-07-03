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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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


def product_comment_create(request, pk):
    """Product 댓글 작성"""

    product = Product.objects.get(pk=pk)
    product_comment_form = ProductCommentForm(request.POST, request.FILES)
    product_recomment_form = ProductRecommentForm(request.POST)
    product_comment_imgs = request.FILES.getlist("file")

    if product_comment_form.is_valid():
        # product comment save
        product_comment = product_comment_form.save(commit=False)
        consumer = Consumer.objects.get(user=request.user)
        product_comment.consumer = consumer
        product_comment.product = product
        product_comment.get_rating_avg()
        product_comment.save()
        product.reviews += 1

        # Product_Comment_Image
        for img in product_comment_imgs:
            images = Product_Comment_Image.objects.create(
                product_comment=product_comment, image=img
            )
            images.save()

        # freshness
        if product_comment.freshness == 1:
            product.freshness_1 += 1
        elif product_comment.freshness == 3:
            product.freshness_3 += 1
        else:
            product.freshness_5 += 1

        # flavor
        if product_comment.flavor == 1:
            product.flavor_1 += 1
        elif product_comment.flavor == 3:
            product.flavor_3 += 1
        else:
            product.flavor_5 += 1

        # cost_performance
        if product_comment.cost_performance == 1:
            product.cost_performance_1 += 1
        elif product_comment.cost_performance == 3:
            product.cost_performance_3 += 1
        else:
            product.cost_performance_5 += 1

        # total rating calculate
        product.calculate_total_rating_sum(product_comment.avg)
        result = product.calculate_total_rating_avg()

        # specific rating calculate
        product.calculate_specific_rating(
            product_comment.freshness, product_comment.flavor, product_comment.cost_performance
        )

    return redirect(reverse("comments:product_comment_detail", args=[pk]))


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
        "user_image": author.profile_image.url,
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
        "user_image": author.profile_image.url,
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
        "user_image": author.profile_image.url,
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

from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from comments.models import Editor_Review_Comment, Editor_Review_Recomment
from editor_reviews.models import Editor_Review
from .models import EditorReviewCommentLike, EditorReviewRecommentLike, EditorReviewLike
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# Create your views here.
@require_POST
@login_required
def EditorReviewLike(request):
    if request.is_ajax():
        pk = request.POST.get("pk")
        post = Editor_Review.objects.get(pk=pk)
        is_like = True

        try:
            like = EditorReviewLike.objects.get(user=request.user, review=post)
            like.delete()
            is_like = False

        except ObjectDoesNotExist:
            new_like = EditorReviewLike(user=request.user, review=post)
            new_like.save()

        ctx = {
            "likes": EditorReviewLike.objects.filter(review=post).count(),
            "status": is_like,
        }

        return JsonResponse(ctx)


def EditorReviewCommentLikeView(request):
    if request.is_ajax():
        if request.user == AnonymousUser():
            return HttpResponse("로그인 후 좋아요 할 수 있습니다.", status=403)

        else:
            pk = request.POST.get("pk")
            comment = Editor_Review_Comment.objects.get(pk=pk)
            is_like = True

            try:
                like = EditorReviewCommentLike.objects.get(
                    user=request.user, comment=comment
                )

                like.delete()
                is_like = False

            except ObjectDoesNotExist:
                new_like = EditorReviewCommentLike(user=request.user, comment=comment)
                new_like.save()

            ctx = {
                "likes": EditorReviewCommentLike.objects.filter(
                    comment=comment
                ).count(),
                "status": is_like,
            }

            return JsonResponse(ctx)

    return redirect(reverse("core:home"))


def EditorReviewRecommentLikeView(request):
    if request.is_ajax():
        if request.user == AnonymousUser():
            return HttpResponse("로그인 후 좋아요 할 수 있습니다.", status=403)

        else:
            pk = request.POST.get("pk")
            comment = Editor_Review_Recomment.objects.get(pk=pk)
            is_like = True

            try:
                like = EditorReviewRecommentLike.objects.get(
                    user=request.user, recomment=comment
                )

                like.delete()
                is_like = False

            except ObjectDoesNotExist:
                new_like = EditorReviewRecommentLike(
                    user=request.user, recomment=comment
                )
                new_like.save()

            ctx = {
                "likes": EditorReviewRecommentLike.objects.filter(
                    recomment=comment
                ).count(),
                "status": is_like,
            }

            return JsonResponse(ctx)

    return redirect(reverse("core:home"))

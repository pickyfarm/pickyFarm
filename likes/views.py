from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from comments.models import (
    Editor_Review_Comment,
    Editor_Review_Recomment,
    Farmer_Story_Comment,
    Farmer_Story_Recomment,
)
from .models import (
    EditorReviewCommentLike,
    EditorReviewRecommentLike,
    FarmerStoryCommentLike,
    FarmerStoryRecommentLike,
)
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist


# editor's review
def EditorReviewCommentLikeView(request):
    if request.is_ajax():
        if request.user == AnonymousUser():
            return HttpResponse("로그인 후 좋아요 할 수 있습니다.", status=403)

        else:
            pk = request.POST.get("pk")
            comment = Editor_Review_Comment.objects.get(pk=pk)
            is_like = True

            try:
                like = EditorReviewCommentLike.objects.get(user=request.user, comment=comment)

                like.delete()
                is_like = False

            except ObjectDoesNotExist:
                new_like = EditorReviewCommentLike(user=request.user, comment=comment)
                new_like.save()

            ctx = {
                "likes": EditorReviewCommentLike.objects.filter(comment=comment).count(),
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
                like = EditorReviewRecommentLike.objects.get(user=request.user, recomment=comment)

                like.delete()
                is_like = False

            except ObjectDoesNotExist:
                new_like = EditorReviewRecommentLike(user=request.user, recomment=comment)
                new_like.save()

            ctx = {
                "likes": EditorReviewRecommentLike.objects.filter(recomment=comment).count(),
                "status": is_like,
            }

            return JsonResponse(ctx)

    return redirect(reverse("core:home"))


# farmer story
def FarmerStoryCommentLikeView(request):
    if request.is_ajax():
        if request.user == AnonymousUser():
            return HttpResponse("로그인 후 좋아요 할 수 있습니다.", status=403)

        else:
            pk = request.POST.get("pk")
            comment = Farmer_Story_Comment.objects.get(pk=pk)
            is_like = True

            try:
                like = FarmerStoryCommentLike.objects.get(user=request.user, comment=comment)

                like.delete()
                is_like = False

            except ObjectDoesNotExist:
                new_like = FarmerStoryCommentLike(user=request.user, comment=comment)
                new_like.save()

            ctx = {
                "likes": FarmerStoryCommentLike.objects.filter(comment=comment).count(),
                "status": is_like,
            }

            return JsonResponse(ctx)

    return redirect(reverse("core:home"))


def FarmerStoryRecommentLikeView(request):
    if request.is_ajax():
        if request.user == AnonymousUser():
            return HttpResponse("로그인 후 좋아요 할 수 있습니다.", status=403)

        else:
            pk = request.POST.get("pk")
            comment = Farmer_Story_Recomment.objects.get(pk=pk)
            is_like = True

            try:
                like = FarmerStoryRecommentLike.objects.get(user=request.user, recomment=comment)

                like.delete()
                is_like = False

            except ObjectDoesNotExist:
                new_like = FarmerStoryRecommentLike(user=request.user, recomment=comment)
                new_like.save()

            ctx = {
                "likes": FarmerStoryRecommentLike.objects.filter(recomment=comment).count(),
                "status": is_like,
            }

            return JsonResponse(ctx)

    return redirect(reverse("core:home"))

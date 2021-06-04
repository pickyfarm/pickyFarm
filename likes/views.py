from django.shortcuts import render
from django.http import JsonResponse
from comments.models import Editor_Review_Comment, Editor_Review_Recomment
from .models import EditorReviewCommentLike, EditorReviewRecommentLike

# Create your views here.
def EditorReviewCommentLikeView(request):
    if request.is_ajax():
        pk = request.POST.get("pk")
        comment = Editor_Review_Comment.objects.get(pk=pk)

        new_like = EditorReviewCommentLike(user=request.user, comment=comment)
        new_like.save()

        like_count = EditorReviewCommentLike.objects.filter(comment=comment).count()

        ctx = {
            "likes": like_count,
        }

        return JsonResponse(ctx)


def EditorReviewRecommentLikeView(request):
    if request.is_ajax():
        pk = request.POST.get("pk")
        comment = Editor_Review_Recomment.objects.get(pk=pk)

        new_like = EditorReviewRecommentLike(user=request.user, comment=comment)
        new_like.save()

        like_count = EditorReviewRecommentLike.objects.filter(comment=comment).count()

        ctx = {
            "likes": like_count,
        }

        return JsonResponse(ctx)

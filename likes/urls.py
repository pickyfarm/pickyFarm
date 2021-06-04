from django.urls import path
from django.conf.urls import include, url
from . import views

app_name = "likes"

urlpatterns = [
    path(
        "editor_review_comment/",
        views.EditorReviewCommentLikeView,
        name="editor_review_comment_like",
    ),
    path(
        "editor_review_recomment/",
        views.EditorReviewRecommentLikeView,
        name="editor_review_recomment_like",
    ),
]

from django.urls import path
from . import views


app_name = "editors_pick"

urlpatterns = [
    path("list/", views.index, name="index"),
    path("create/", views.create, name="create"),
    #
    # editor's pick 세부 포스팅
    #
    path("<int:pk>/", views.Editor_review_detail.as_view(), name="detail"),
    path("<int:pk>/comment/", views.editor_review_comment, name="comment"),
    #
    # editor's pick comment 관련 AJAX urls
    #
    path(
        "<int:reviewpk>/comment/edit/<int:commentpk>",
        views.editor_review_comment_edit,
        name="comment_edit",
    ),
    path(
        "<int:reviewpk>/comment/delete/<int:commentpk>",
        views.editor_review_comment_delete,
        name="comment_delete",
    ),
    path(
        "<int:reviewpk>/comment/<int:commentpk>/recomment",
        views.editor_review_recomment,
        name="recomment",
    ),
    path("recomment/edit/", views.editor_review_recomment_edit, name="recomment_edit"),
    path("recomment/delete/", views.editor_review_recomment_delete, name="recomment_delete"),
    path("<int:pk>/update/", views.update, name="update"),
    path("delete/", views.delete, name="delete"),
]
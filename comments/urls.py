from django.urls import path
from comments import views

app_name = "comments"

urlpatterns = [
    # product comment
    path(
        "product_comment/<int:pk>/recomment/",
        views.product_recomment_detail,
        name="product_recomment_detail",
    ),
    # product recomment
    path(
        "product/<int:productpk>/comment/<int:commentpk>/recomment/",
        views.product_recomment,
        name="product_recomment",
    ),
    path(
        "product/recomment/edit/",
        views.product_recomment_edit,
        name="product_recomment_edit",
    ),
    path(
        "product/recomment/delete/",
        views.product_recomment_delete,
        name="product_recomment_delete",
    ),
    # editors_review
    # path('editors_review_comment/<int:pk>/', views.editors_review_comment, name="editors_review_comment"),
    # path('editors_review_comment/<int:pk>/recomment/', views.editors_review_recomment, name="editors_review_recomment"),
    # farmer's story comment
    path(
        "farmer_story/<int:pk>/comment/create/",
        views.farmer_story_comment,
        name="farmer_story_comment",
    ),
    path(
        "farmer_story/<int:storypk>/comment/edit/<int:commentpk>/",
        views.farmer_story_comment_edit,
        name="farmer_story_comment_edit",
    ),
    path(
        "farmer_story/<int:storypk>/comment/delete/<int:commentpk>/",
        views.farmer_story_comment_delete,
        name="farmer_story_comment_delete",
    ),
    path("farmer_story/comment/more/", views.farmer_story_comment_load, name="story_comment_load"),
    # farmer's story recomment
    path(
        "farmer_story/<int:storypk>/comment/<int:commentpk>/recomment/",
        views.farmer_story_recomment,
        name="farmer_story_recomment",
    ),
    path(
        "farmer_story/recomment/edit/",
        views.farmer_story_recomment_edit,
        name="farmer_story_recomment_edit",
    ),
    path(
        "farmer_story/recomment/delete/",
        views.farmer_story_recomment_delete,
        name="farmer_story_recomment_delete",
    ),
    path(
        "farmer_story/recomment/more/",
        views.farmer_story_recomment_load,
        name="story_recomment_load",
    ),
]

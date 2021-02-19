from django.urls import path
from comments import views

app_name = "comments"

urlpatterns = [
    # product
    path('product_comment/<int:pk>/', views.product_comment_detail, name="product_comment_detail"),
    path('product_comment/<int:pk>/recomment/', views.product_recomment_detail, name="product_recomment_detail"),
    path('product_comment/<int:pk>/recomment/create', views.product_recomment_create, name="product_recomment_create"),
    
    # editors_review
    # path('editors_review_comment/<int:pk>/', views.editors_review_comment, name="editors_review_comment"),
    # path('editors_review_comment/<int:pk>/recomment/', views.editors_review_recomment, name="editors_review_recomment"),
]

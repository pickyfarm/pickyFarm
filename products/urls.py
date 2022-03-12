from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("list/", views.StoreList.as_view(), name="store_list"),
    path("list/<slug:cat>/", views.store_list_cat, name="store_list_category"),
    path("detail/<int:pk>/", views.product_detail, name="product_detail"),
    path("detail/qna_paginator/", views.question_paging, name="qna_paginator"),
    # path('enroll/', views.product_enroll, name="product_enroll"),
    # path('delete/<int:pk>/', views.product_delete, name="product_delete"),
    # path('update/<int:pk>/', views.product_update, name="product_update"),
    path("question/create", views.create_question, name="question_create"),
    path("question/<int:pk>", views.read_qna, name="question_read"),
    # pagination
    path("detail/<int:pk>/comment_ajax/", views.comment_ajax, name="comment_ajax"),
    path("detail/<int:pk>/question_ajax/", views.question_ajax, name="question_ajax"),
    path("get-db", views.get_product_EP, name="get_product_db"),
    path("test-list/", views.new_product_page, name="new_product_test"),
]

from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('list/', views.store_list_all, name="store_list"),
    path('list/<slug:cat>/', views.store_list_cat, name="store_list_category"),
    path('detail/<int:pk>/', views.product_detail, name="product_detail"),
    path('detail/qna_paginator/', views.question_paging, name="qna_paginator"),
    #path('enroll/', views.product_enroll, name="product_enroll"),
    #path('delete/<int:pk>/', views.product_delete, name="product_delete"),
    #path('update/<int:pk>/', views.product_update, name="product_update"),
    path('question/create', views.create_question, name="question_create"),
]

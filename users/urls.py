from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('farmers_page/', views.farmers_page, name='farmers_page'),
    path('farmer_detail/<int:pk>/', views.farmer_detail, name='farmer_detail'),
    path('cart_in/<int:product_pk>/', views.cart_in, name="cart_in"),
]
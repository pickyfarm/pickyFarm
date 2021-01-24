from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('farmers_page/', views.farmers_page, name='farmers_page'),
    path('farmer_detail/<int:pk>/', views.farmer_detail, name='farmer_detail'),
    path('cart_in/<int:product_pk>/', views.cart_in, name="cart_in"),
    path('wish/<int:product_pk>/', views.wish, name='wish'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
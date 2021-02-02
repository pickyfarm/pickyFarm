from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('farmers_page/', views.farmers_page, name='farmers_page'),
    path('farmers_page/farmer_search/', views.farmer_search, name='farmer_search'),
    path('farmers_page/farmer_story_search/', views.farmer_story_search, name='farmer_story_search'),
    path('farmer_detail/<int:pk>/', views.farmer_detail, name='farmer_detail'),
    path('cart_in/<int:product_pk>/', views.cart_in, name="cart_in"),
    path('wish/<int:product_pk>/', views.wish, name='wish'),
]
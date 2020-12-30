from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('farmers_page/', views.farmers_page, name='farmers_page'),
    path('farmer_detail/<int:pk>/', views.farmer_detail, name='farmer_detail'),
]
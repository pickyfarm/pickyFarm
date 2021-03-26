from django.urls import path, include
from . import views


app_name = 'orders'

urlpatterns = [
   path('orderingCart/', views.orderingCart, name="ordering_cart"),
   path('payment/create', views.payment_create, name="payment_create"),
   path('payment/', views.payment, name="payment"),
]
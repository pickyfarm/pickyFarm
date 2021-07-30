from django.urls import path, include
from . import views


app_name = 'orders'

urlpatterns = [
   path('orderingCart/', views.orderingCart, name="ordering_cart"),
   path('payment/update/<int:pk>/', views.payment_update, name="payment_update"),
   path('payment/', views.payment_create, name="payment_create"),
   path('payment/success', views.payment_success, name="payment_success"),
   path('payemnt/fail', views.payment_fail, name="payment_fail"),
   path('payment/valid', views.payment_valid, name="payment_valid"),

   # 주문/결제 완료 페이지 작업하기 위한 임시 url
   # path('temporary/payment/success', views.temporary_payment_success, name="temporary_payment_success")
]
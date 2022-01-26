from django.urls import path, include
from . import views


app_name = "orders"

urlpatterns = [
    path("orderingCart/", views.orderingCart, name="ordering_cart"),
    path("payment/update/<int:pk>/", views.payment_update, name="payment_update"),
    path("payment/", views.payment_create, name="payment_create"),
    path("payment/change-address", views.changeAddressAjax, name="payment_change-address"),
    # path('payment/success', views.payment_success, name="payment_success"),
    path("payment/fail", views.payment_fail, name="payment_fail"),
    path("payment/valid", views.payment_valid, name="payment_valid"),
    path("payment/vbank-progress", views.vbank_progess, name="vbank_progess"),
    path("payment/vbank-deposit", views.vbank_deposit, name="vbank_deposit"),
    path(
        "payment/vbank-template-test",
        views.vbank_template_test,
        name="vbank_template_test",
    ),
    path("payment/cancel/<int:pk>", views.order_cancel, name="payment_cancel"),
    # path('payment_fail', views.fail_test, name="fail_test"), 결제취소 창 테스트용 path
    path("change-refund/<int:pk>", views.create_change_or_refund, name="change_refund"),
    path("payment/subscribe", views.sub_modal, name="payment_success_modal"),
    path("payment/gift", views.payment_create_gift, name="payment_gift"),
    path("payment/gift/update", views.payment_update_gift, name="payment_gift_update"),
    path("payment/gift/valid", views.payment_valid_gift, name="payment_gift_valid"),
    path(
        "payment/gift/popup/address",
        views.delivery_address_update,
        name="payment_gift_delivery_update",
    ),
    path(
        "payment/gift/popup/order",
        views.payment_gift_order_list_popup,
        name="payment_gift_order_list",
    ),
    path(
        "payment/calculate-delivery-fee",
        views.calculate_delivery_fee,
        name="calculate_delivery_fee",
    ),
]

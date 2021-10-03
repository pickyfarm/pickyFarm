from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = "farmers"

urlpatterns = [
    path("", views.farmers_page, name="farmers_page"),
    path("farmer_search/", views.farmer_search, name="farmer_search"),
    path("farmer_story_search/", views.farmer_story_search, name="farmer_story_search"),
    path(
        "farmer_story/detail/<int:pk>/",
        views.Story_Detail.as_view(),
        name="farmer_story_detail",
    ),
    path(
        "farmer_story/create/", views.farmer_story_create, name="farmer_story_create"
    ),  # 추후 url 경로 수정하기
    path("farm_cat_search/", views.farm_cat_search, name="farm_cat_search"),
    path("farm_tag_search/", views.farm_tag_search, name="farm_tag_search"),
    path("farmer_detail/<int:pk>/", views.farmer_detail, name="farmer_detail"),
    path("apply/", views.farm_apply, name="farm_apply"),
    path("enroll/step/1/", views.enroll_page1, name="enroll_page1"),
    path("enroll/step/2/<int:consumerpk>/", views.enroll_page2, name="enroll_page2"),
    path("enroll/step/3/<int:farmerpk>/", views.enroll_page3, name="enroll_page3"),
    path("enroll/login", views.FarmEnrollLogin.as_view(), name="farm_enroll_login"),
    # farmer mypage
    path(
        "mypage/info/update",
        views.FarmerMyPageInfoManage.as_view(),
        name="farmer_mypage_info_update",
    ),
    path(
        "mypage/products/",
        views.FarmerMyPageProductManage.as_view(),
        name="farmer_mypage_product",
    ),
    path(
        "mypage/orders",
        views.FarmerMyPageOrderManage.as_view(),
        name="farmer_mypage_order",
    ),
    path(
        "mypage/orders/state",
        views.farmer_mypage_order_state_update,
        name="farmer_mypage_order_state_update",
    ),
    path(
        "mypage/payment",
        views.FarmerMyPagePaymentManage.as_view(),
        name="farmer_mypage_payment",
    ),
    path(
        "mypage/notifications",
        views.FarmerMyPageNotificationManage.as_view(),
        name="farmer_mypage_notification",
    ),
    path(
        "mypage/reviews-qnas",
        views.FarmerMyPageReviewQnAManage.as_view(),
        name="farmer_mypage_review_qna",
    ),
    path(
        "mypage/reviews-qnas/<int:pk>/answer",
        views.FarmerMypageQuestionAnswer.as_view(),
        name="farmer_mypage_question_answer",
    ),
    path(
        "mypage/notice", views.FarmerMyPageNotice.as_view(), name="farmer_mypage_notice"
    ),
    # mypage pagination ajax url
    path(
        "mypage/notifications/notification_ajax/",
        views.notification_ajax,
        name="notification_ajax",
    ),
    path("mypage/reviews-qnas/qna-ajax/", views.qna_ajax, name="qna_ajax"),
    path("mypage/reviews-qnas/review-ajax/", views.review_ajax, name="review_ajax"),
    # mypage popups url
    path(
        "mypage/orders/check/",
        views.FarmerMyPageOrderCheckPopup.as_view(),
        name="farmer_mypage_order_check_popup",
    ),
    path(
        "mypage/orders/cancel/<int:pk>",
        views.FarmerMypageOrderCancelPopup.as_view(),
        name="farmer_mypage_order_cancel_popup",
    ),
    path(
        "mypage/orders/invoice/<int:pk>",
        views.FarmerMypageInvoiceUpdatePopup.as_view(),
        name="farmer_mypage_invoice_update_popup",
    ),
    path(
        "mypage/product/update",
        views.FarmerMypageProductUpdatePopup.as_view(),
        name="farmer_mypage_product_update",
    ),
    path(
        "mypage/product/update/<int:pk>",
        views.FarmerMypPageProductStateUpdate.as_view(),
        name="farmer_mypage_product_state_update",
    ),
    path(
        "mypage/orders/<int:pk>/refund/request/check/",
        views.FarmerMyPageRefundRequestCheckPopup.as_view(),
        name="farmer_mypage_refund_check_popup",
    ),
    path(
        "mypage/orders/<int:pk>/exchange/request/check/",
        views.FarmerMyPageExchangeRequestCheckPopup.as_view(),
        name="farmer_mypage_exchange_check_popup",
    ),
    path(
        "mypage/popup-callback",
        views.FarmerMypagePopupCallback.as_view(),
        name="popup_callback",
    ),
]

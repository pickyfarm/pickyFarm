from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = "farmers"

urlpatterns = [
    path("", views.farmers_page, name="farmers_page"),
    path("farmer_search/", views.farmer_search, name="farmer_search"),
    path("farmer_story_search/", views.farmer_story_search, name="farmer_story_search"),
    path("diary/create", views.farmer_story_create, name="farmer_story_create"),  # 추후 url 경로 수정하기
    path("diary/<int:pk>/update", views.farmer_story_update, name="farmer_story_update"),
    path("diary/<int:pk>", views.Story_Detail.as_view(), name="farmer_story_detail"),
    path("farm_cat_search/", views.farm_cat_search, name="farm_cat_search"),
    path("farm_tag_search/", views.farm_tag_search, name="farm_tag_search"),
    path("farmer_detail/<int:pk>/", views.farmer_detail, name="farmer_detail"),
    path(
        "farmer_detail/<int:pk>/products_ajax/",
        views.products_ajax,
        name="products_ajax",
    ),
    path(
        "farmer_detail/<int:pk>/diary_ajax/",
        views.diary_ajax,
        name="diary_ajax",
    ),
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
    path("mypage/info/farm_news/", views.farm_news_update, name="farm_news_update"),
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
        "mypage/notifications/",
        views.FarmerMyPageNotificationManage.as_view(),
        name="farmer_mypage_notification",
    ),
    path(
        "mypage/reviews-qnas/",
        views.FarmerMyPageReviewQnAManage.as_view(),
        name="farmer_mypage_review_qna",
    ),
    path(
        "mypage/reviews-qnas/<int:pk>/answer",
        views.FarmerMypageQuestionAnswer.as_view(),
        name="farmer_mypage_question_answer",
    ),
    path(
        "mypage/reviews-qnas/review/<int:pk>/answer",
        views.FarmerMypageReviewAnswer.as_view(),
        name="farmer_mypage_review_answer",
    ),
    path("mypage/notice", views.FarmerMyPageNotice.as_view(), name="farmer_mypage_notice"),
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
        "mypage/orders/list_excel",
        views.FarmerMypageGetOrderList.as_view(),
        name="farmer_mypage_get_order_list",
    ),
    path(
        "mypage/orders/list_excel_ajax",
        views.get_order_list_excel,
        name="farmer_mypage_get_order_list_ajax",
    ),
    path(
        "mypage/orders/check",
        views.FarmerMyPageOrderCheckPopup.as_view(),
        name="farmer_mypage_order_check_popup",
    ),
    path(
        "mypage/orders/cancel",
        views.FarmerMypageOrderCancelPopup.as_view(),
        name="farmer_mypage_order_cancel_popup",
    ),
    path(
        "mypage/orders/invoice",
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
        views.FarmerMyPageProductStateUpdate.as_view(),
        name="farmer_mypage_product_state_update",
    ),
    path(
        "mypage/orders/refund/request/check",
        views.FarmerMyPageRefundRequestCheckPopup.as_view(),
        name="farmer_mypage_refund_check_popup",
    ),
    path(
        "mypage/orders/exchange/request/check",
        views.FarmerMyPageExchangeRequestCheckPopup.as_view(),
        name="farmer_mypage_exchange_check_popup",
    ),
    path(
        "mypage/popup-callback",
        views.FarmerMypagePopupCallback.as_view(),
        name="popup_callback",
    ),
    path("modal/farmer-sub", views.farmer_subs_modal, name="farmer_subs_modal"),
]

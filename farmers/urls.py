from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = "farmers"

urlpatterns = [
    path("", views.farmers_page, name="farmers_page"),
    path("farmer_search/", views.farmer_search, name="farmer_search"),
    path("farmer_story_search/", views.farmer_story_search, name="farmer_story_search"),
    path("farmer_story/detail/<int:pk>/", views.Story_Detail.as_view(), name="farmer_story_detail"),
    path(
        "farmer_story/create/", views.farmer_story_create, name="farmer_story_create"
    ),  # 추후 url 경로 수정하기
    path("farm_cat_search/", views.farm_cat_search, name="farm_cat_search"),
    path("farm_tag_search/", views.farm_tag_search, name="farm_tag_search"),
    path("farmer_detail/<int:pk>/", views.farmer_detail, name="farmer_detail"),
    path("apply/", views.farm_apply, name="farm_apply"),
    path("enroll/step/<int:step>/", views.FarmEnroll.as_view(), name="farm_enroll"),
    # farmer mypage
    path(
        "mypage/info/update/",
        views.FarmerMyPageInfoManage.as_view(),
        name="farmer_mypage_info_update",
    ),
    path(
        "mypage/products/", views.FarmerMyPageProductManage.as_view(), name="farmer_mypage_product"
    ),
    path("mypage/orders", views.FarmerMyPageOrderManage.as_view(), name="farmer_mypage_order"),
    path(
        "mypage/notifications/",
        views.FarmerMyPageNotificationManage.as_view(),
        name="farmer_mypage_notification",
    ),
    path(
        "mypage/reviews_qnas/",
        views.FarmerMyPageReviewQnAManage.as_view(),
        name="farmer_mypage_review_qna",
    ),
    path("mypage/notice", views.FarmerMyPageNotice.as_view(), name="farmer_mypage_notice"),
    # mypage pagination ajax url
    path(
        "mypage/notifications/notification_ajax/",
        views.notification_ajax,
        name="notification_ajax",
    ),
    path("mypage/reviews_qnas/qna_ajax/", views.qna_ajax, name="qna_ajax"),
    path("mypage/reviews_qnas/review_ajax/", views.review_ajax, name="review_ajax"),
]

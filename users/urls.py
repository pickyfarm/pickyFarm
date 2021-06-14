from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("login/kakao/", views.kakao_login, name="kakao_login"),
    path("login/kakao/callback", views.kakao_callback, name="kakao_login_callback"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("signup/id_validation/", views.idValidation, name="id_validation"),
    path(
        "signup/nickname_validation/",
        views.nicknameValidation,
        name="nickname_validation",
    ),
    path("signup/email_validation/", views.emailValidation, name="email_validation"),
    path("password_reset/", views.MyPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.MyPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        views.MyPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.MyPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("mypage/<slug:cat>", views.mypage, name="mypage"),
    path("editor_mypage/", views.EditorMyPage.as_view(), name="editor_mypage"),
    path(
        "editor_mypage/comments",
        views.EditorMyPage_Comments.as_view(),
        name="editor_mypage_comments",
    ),
    path("find_my_id/", views.FindMyIdView.as_view(), name="find_my_id"),
    path(
        "find_my_id/complete", views.FindMyIdView.as_view(), name="find_my_id_complete"
    ),
    path(
        "find_my_id/failed", views.FindMyIdFailView.as_view(), name="find_my_id_failed"
    ),
    path("cartIn/", views.CartInAjax, name="cartInAjax"),
    path("cartOut/", views.cartOutAjax, name="cartOutAjax"),
    path("subs/", views.subs, name="subs"),
    path("cancelSubs/", views.CancelSubs, name="cancelSubs"),
    path("wish/", views.wish, name="wish"),
    path("infoUpdate/", views.infoUpdate, name="infoUpdate"),
    path("profileUpdate/", views.profileUpdate, name="profileUpdate"),
]

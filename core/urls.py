from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="main"),
    path("index-test", views.landing_test, name="landing-test"),
    path("policy/disclaimer", views.disclaimer, name="disclaimer"),
    path("policy/personal-info", views.personal_info_usage, name="personal-info"),
    path("popup-callback", views.PopupCallback.as_view(), name="popup_callback"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

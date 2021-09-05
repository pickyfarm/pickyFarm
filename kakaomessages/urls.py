from django.urls import path, include
from . import views

app_name = "messages"

urlpatterns = [
    path("test", views.message_test, name="message_test"),
]

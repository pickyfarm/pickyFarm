from django.urls import path
from . import views

app_name = "addresses"

urlpatterns = [
    path('delete/', views.delete, name="delete"),
]

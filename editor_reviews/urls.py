from django.urls import path
from . import views


app_name = 'editors_pick'

urlpatterns = [
    path('list/', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.Editor_review_detail.as_view(), name='detail'),
    path('<int:pk>/comment/', views.editor_review_comment, name='comment'),
    path('<int:reviewpk>/comment/delete/<int:commentpk>', views.editor_review_comment_delete, name="comment_delete"),
    path('<int:pk>/update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
]
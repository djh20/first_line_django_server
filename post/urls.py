#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.user_read, name='user_readAll'),
    path('manage/', views.admin_read, name='admin_readAll'),
    path('<int:pk>/', views.user_post, name='user_post'),
]
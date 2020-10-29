#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_reply, name='user_reply'),
    path('manage/', views.admin_reply, name='admin_reply'),
]
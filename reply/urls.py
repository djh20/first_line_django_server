#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
   path('', views.user_process_reply, name='user_process'),
    path('manage/', views.admin_process_reply, name='admin_process'),
    path('manage/blind/',views.admin_blind_reply, name='admin_blind_replies'),
]
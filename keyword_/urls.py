#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('',views.user_process_keyword,name='user_process_keyword'),
    path('manage/', views.process_admin_keyword, name='admin_keyword'),
]
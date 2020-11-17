#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.user_read_login_log, name = 'user_read_login_log'),
    path('manage/', views.admin_process_log, name='admin_process'),
    
]
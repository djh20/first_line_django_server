#backend/post/urls.py
from django.urls import path

from . import views
urlpatterns = [
    path('manage/', views.process_admin_notice,name='manage'),
    path('', views.process_user_notice,name='manage'),
]
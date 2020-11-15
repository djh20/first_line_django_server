#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.process_admin_report, name='admin_reply'),
    path('<int:pk>/', views.read_report, name='read_report'),
    path('manage/process/', views.process_report, name='process_report'),
]
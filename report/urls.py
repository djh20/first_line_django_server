#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.process_admin_report, name='admin_reply'),
    path('<int:pk>/', views.read_report, name='read_report'),
    path('post/', views.report_post, name='report_post'),
    path('reply/', views.report_reply, name='report_reply'),
    path('manage/process/', views.process_report, name='process_report'),
]
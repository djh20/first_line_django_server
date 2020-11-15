#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.process_admin_keyword, name='admin_keyword'),
]
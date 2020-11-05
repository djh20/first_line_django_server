#backend/post/urls.py
from django.urls import path

from . import views
urlpatterns = [
    path('manage/', views.admin_search_notice,name='manage'),
]
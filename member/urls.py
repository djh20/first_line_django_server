#backend/post/urls.py
from django.urls import path

from . import views
urlpatterns = [
    path('login/', views.login,name='login'),
    path('', views.register_user ,name='register')
]
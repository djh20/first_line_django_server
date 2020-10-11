#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.MemberController.readAll, name='readAll'),
]
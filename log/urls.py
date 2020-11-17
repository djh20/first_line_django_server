#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.user_)
    path('manage/', views.admin_process_log, name='admin_process'),
    

]
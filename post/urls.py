#backend/post/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_process_post, name='user_process'),
    path('manage/', views.admin_process_post, name='admin_prosess'),
    path('manage/blind/',views.admin_blind_post, name = 'admin_blind_post'),
    path('<int:pk>/', views.user_read_post, name='user_read_post'),
    path('', views.user_search_post, name='user_search_post'),
    path('like/<int:pk>/', views.user_like_post, name ='user_like_post'),
    path('like/record/',views.user_read_like_post,name='user_read_like_post'),
    path('lookup/record/',views.user_read_lookup_post, name='user_read_lookup_post')
]
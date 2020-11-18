from django.urls import path

from . import views
urlpatterns = [
    path('login/', views.login,name='login'),
    path('change/password/',views.user_change_password,name='user_change_password'),
    path('admin/login/', views.admin_login,name='admin_login'),
    path('', views.user_process_info ,name='user_process_info'),
    path('manage/',views.admin_process_info, name='admin_process_info'),
    path('sementic/',views.user_sementic_process, name='user_process_sementic')
    
]
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'), 
    path('update/<int:id>/', views.task_update, name='task_update'),  
    path('delete/<int:id>/', views.task_delete, name='task_delete'),  
    path('toggle-task/<int:id>/', views.toggle_task, name='toggle_task'),  
    path('login/', views.user_login, name='user_login'),  
    path('logout/', views.user_logout, name='user_logout'), 
    path('register/', views.user_registration, name='register'),
    path('task/<int:id>/detail/', views.task_detail, name='task_detail'),
]

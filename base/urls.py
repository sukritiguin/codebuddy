from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
    path('status/', views.status, name='status'),
    path('status/<int:status_id>/delete/', views.status_delete, name='status_delete'),
    path('status/<int:status_id>/like/', views.like_status, name='like_status'),
    path('status/<int:status_id>/', views.current_status, name='current_status'),
    path('status/<int:status_id>/likes/', views.likes_of_status, name='liked_status'),
    path('status/<int:comment_id>/delete_comment/', views.delete_comment, name='comment_delete'),
]

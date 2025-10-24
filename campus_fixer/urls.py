from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report_issue/', views.report_issue, name='report_issue'),
    path('track_issue/', views.track_issue, name='track_issue'),
    path('update_issue/<str:ticket_id>/', views.update_issue, name='update_issue'),
    path('lost-found-feed/', views.lost_found_feed, name='lost_found_feed'),
]

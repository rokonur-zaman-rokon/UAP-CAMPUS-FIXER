from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Landing / Home page
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('track-issue/', views.track_issue, name='track_issue'),
    path('update-issue/<str:ticket_id>/', views.update_issue, name='update_issue'),
    path('lost-found-feed/', views.lost_found_feed, name='lost_found_feed'),
    path('ajax/resolved-count/', views.issues_resolved_count, name='issues_resolved_count'),
]

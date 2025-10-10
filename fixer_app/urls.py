from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('report/', views.report_issue, name='report_issue'),
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issue/<int:pk>/update/', views.update_issue, name='update_issue'),
]

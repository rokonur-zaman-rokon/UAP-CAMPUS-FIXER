from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.front_page, name='front_page'),  # 👈 new front landing page
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('report/', views.report_issue, name='report_issue'),
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issue/<int:pk>/update/', views.update_issue, name='update_issue'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='front_page'), name='logout'),
    path('login/', views.login_view, name='login'),

]

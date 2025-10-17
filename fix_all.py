import os
import shutil
import subprocess

def fix_project_structure():
    print("🔧 Fixing project structure...")
    
    # Create correct directory structure
    directories = [
        "campus_fixer/templates/campus_fixer",
        "campus_fixer/static/campus_fixer/css",
        "campus_fixer/static/campus_fixer/js",
        "campus_fixer/static/campus_fixer/images",
        "media/issues"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    # Fix file names
    if os.path.exists("campus_fixer/report_lissue.html"):
        os.rename("campus_fixer/report_lissue.html", "campus_fixer/templates/campus_fixer/report_issue.html")
    
    if os.path.exists("campus_fixer/track_lissue.html"):
        os.rename("campus_fixer/track_lissue.html", "campus_fixer/templates/campus_fixer/track_issue.html")

def create_correct_views():
    print("📝 Creating correct views.py...")
    
    views_content = '''from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request, 'campus_fixer/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'campus_fixer/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'campus_fixer/dashboard.html')

@login_required
def report_issue(request):
    return render(request, 'campus_fixer/report_issue.html')

@login_required
def track_issue(request, ticket_id=None):
    return render(request, 'campus_fixer/track_issue.html')

def admin_dashboard(request):
    return render(request, 'campus_fixer/admin_dashboard.html')
'''
    
    with open("campus_fixer/views.py", 'w', encoding='utf-8') as f:
        f.write(views_content)
    print("✅ views.py created")

def create_urls():
    print("🔗 Creating urls.py...")
    
    # Project urls.py
    project_urls = '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('campus_fixer.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    
    with open("uap_campus_fixer/urls.py", 'w', encoding='utf-8') as f:
        f.write(project_urls)
    
    # App urls.py
    app_urls = '''from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='campus_fixer/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('track-issue/', views.track_issue, name='track_issue'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
'''
    
    with open("campus_fixer/urls.py", 'w', encoding='utf-8') as f:
        f.write(app_urls)
    print("✅ urls.py created")

def create_models():
    print("🗃️ Creating models.py...")
    
    models_content = '''from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class UserProfile(models.Model):
    USER_TYPES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    department = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class Issue(models.Model):
    DEPARTMENTS = [
        ('CSE', 'CSE'),
        ('EEE', 'EEE'),
        ('ARCHITECTURE', 'Architecture'),
        ('CIVIL', 'Civil Engineering'),
        ('BBA', 'BBA'),
        ('ENGLISH', 'English'),
        ('LAW', 'Law'),
        ('PHARMACY', 'Pharmacy'),
        ('OTHERS', 'Others'),
    ]
    
    CATEGORIES = [
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('cleanliness', 'Cleanliness'),
        ('it', 'IT'),
        ('furniture', 'Furniture'),
        ('safety', 'Safety'),
        ('lost_found', 'Lost & Found'),
        ('suggestions', 'Suggestions'),
        ('others', 'Others'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    ticket_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=UserProfile.USER_TYPES)
    department = models.CharField(max_length=20, choices=DEPARTMENTS)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='issues/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.ticket_id} - {self.category}"
'''
    
    with open("campus_fixer/models.py", 'w', encoding='utf-8') as f:
        f.write(models_content)
    print("✅ models.py created")

def create_forms():
    print("📋 Creating forms.py...")
    
    forms_content = '''from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES)
    department = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'department', 'phone_number')
'''
    
    with open("campus_fixer/forms.py", 'w', encoding='utf-8') as f:
        f.write(forms_content)
    print("✅ forms.py created")

def update_settings():
    print("⚙️ Updating settings.py...")
    
    try:
        with open("uap_campus_fixer/settings.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add campus_fixer to INSTALLED_APPS
        if "'campus_fixer'" not in content:
            content = content.replace(
                "INSTALLED_APPS = [",
                "INSTALLED_APPS = [\n    'campus_fixer',"
            )
        
        # Add static files configuration
        if "STATICFILES_DIRS" not in content:
            static_config = '''
import os
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "campus_fixer/static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'index'
'''
            content = content.replace(
                "STATIC_URL = 'static/'",
                "STATIC_URL = 'static/'" + static_config
            )
        
        with open("uap_campus_fixer/settings.py", 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ settings.py updated")
        
    except Exception as e:
        print(f"❌ Error updating settings: {e}")

def create_base_template():
    print("🎨 Creating base template...")
    
    base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UAP Campus Fixer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem 0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .nav { display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 1.5rem; font-weight: bold; }
        .nav-links { display: flex; list-style: none; gap: 2rem; }
        .nav-links a { color: white; text-decoration: none; }
        .hero { background: #3498db; color: white; padding: 100px 0; text-align: center; }
        .btn { display: inline-block; padding: 12px 24px; background: #e74c3c; color: white; 
               text-decoration: none; border-radius: 5px; margin: 0 10px; }
        .card { background: white; padding: 2rem; margin: 2rem 0; border-radius: 10px; }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <nav class="nav">
                <div class="logo">UAP Campus Fixer</div>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/register">Register</a></li>
                    <li><a href="/login">Login</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container">
        {% block content %}
        {% endblock %}
    </main>
</body>
</html>'''
    
    with open("campus_fixer/templates/campus_fixer/base.html", 'w', encoding='utf-8') as f:
        f.write(base_html)
    print("✅ base.html created")

def create_index_template():
    print("🏠 Creating index template...")
    
    index_html = '''{% extends 'campus_fixer/base.html' %}

{% block content %}
<section class="hero">
    <h1>UAP Campus Fixer</h1>
    <p>Simplifying Campus Maintenance Requests</p>
    <div style="margin-top: 2rem;">
        <a href="/register" class="btn">Get Started</a>
        <a href="/login" class="btn">Login</a>
    </div>
</section>

<div class="card">
    <h2>Welcome to UAP Campus Fixer</h2>
    <p>Report and track maintenance issues easily.</p>
</div>
{% endblock %}'''
    
    with open("campus_fixer/templates/campus_fixer/index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("✅ index.html created")

def run_migrations():
    print("🗃️ Running migrations...")
    try:
        subprocess.run(["python", "manage.py", "makemigrations"], check=True)
        subprocess.run(["python", "manage.py", "migrate"], check=True)
        print("✅ Migrations completed")
    except subprocess.CalledProcessError:
        print("⚠️ Migration issues - but continuing")

def main():
    print("🚀 COMPLETE PROJECT FIX")
    print("=" * 50)
    
    steps = [
        ("Fixing structure", fix_project_structure),
        ("Creating views", create_correct_views),
        ("Creating URLs", create_urls),
        ("Creating models", create_models),
        ("Creating forms", create_forms),
        ("Updating settings", update_settings),
        ("Creating base template", create_base_template),
        ("Creating index template", create_index_template),
        ("Running migrations", run_migrations),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        step_func()
    
    print("\n" + "=" * 50)
    print("🎉 FIX COMPLETED!")
    print("\n🚀 Now run:")
    print("python manage.py runserver")
    print("Then visit: http://127.0.0.1:8000/")

if __name__ == "__main__":
    main()
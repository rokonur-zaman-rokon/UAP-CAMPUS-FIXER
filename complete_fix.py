import os
import subprocess
import sys

def run_command(command):
    """Run a shell command"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e.stderr}")
        return False

def create_files():
    print("🚀 Creating all necessary files...")
    
    # Create directories
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

    # 1. Create proper views.py
    views_content = '''from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def index(request):
    """Home page view"""
    return render(request, 'campus_fixer/index.html')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'campus_fixer/register.html', {'form': form})

def custom_login(request):
    """Custom login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'campus_fixer/login.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard"""
    return render(request, 'campus_fixer/dashboard.html')

@login_required
def report_issue(request):
    """Report issue page"""
    return render(request, 'campus_fixer/report_issue.html')

@login_required
def track_issue(request):
    """Track issue page"""
    return render(request, 'campus_fixer/track_issue.html')

@login_required
def admin_dashboard(request):
    """Admin dashboard"""
    return render(request, 'campus_fixer/admin_dashboard.html')
'''

    with open('campus_fixer/views.py', 'w', encoding='utf-8') as f:
        f.write(views_content)
    print("✅ views.py created")

    # 2. Create urls.py for the app
    urls_content = '''from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('track-issue/', views.track_issue, name='track_issue'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
'''

    with open('campus_fixer/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    print("✅ campus_fixer/urls.py created")

    # 3. Update project urls.py
    project_urls_content = '''from django.contrib import admin
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

    with open('uap_campus_fixer/urls.py', 'w', encoding='utf-8') as f:
        f.write(project_urls_content)
    print("✅ uap_campus_fixer/urls.py updated")

    # 4. Update settings.py
    print("⚙️ Updating settings.py...")
    try:
        with open('uap_campus_fixer/settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add campus_fixer to INSTALLED_APPS
        if "'campus_fixer'" not in content:
            content = content.replace(
                "INSTALLED_APPS = [",
                "INSTALLED_APPS = [\n    'campus_fixer',"
            )
        
        # Add static and media config
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
LOGIN_URL = 'login'
'''
            content = content.replace(
                "STATIC_URL = 'static/'",
                "STATIC_URL = 'static/'" + static_config
            )
        
        with open('uap_campus_fixer/settings.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ settings.py updated")
    except Exception as e:
        print(f"❌ Error updating settings: {e}")

    # 5. Create base template
    base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UAP Campus Fixer - {% block title %}Home{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f8f9fa; 
            color: #333;
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header { 
            background: #2c3e50; 
            color: white; 
            padding: 1rem 0; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 0 20px; 
        }
        .nav { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
        }
        .logo { 
            font-size: 1.5rem; 
            font-weight: bold; 
            color: #3498db;
        }
        .nav-links { 
            display: flex; 
            list-style: none; 
            gap: 1.5rem; 
        }
        .nav-links a { 
            color: white; 
            text-decoration: none; 
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .nav-links a:hover { 
            background: rgba(255,255,255,0.1);
        }
        .hero { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 100px 0; 
            text-align: center; 
            flex-grow: 1;
        }
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        .hero p {
            font-size: 1.2rem;
            max-width: 600px;
            margin: 0 auto 2rem;
            opacity: 0.9;
        }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            margin: 0 10px;
            transition: all 0.3s;
        }
        .btn:hover {
            background: #2980b9;
            transform: translateY(-2px);
        }
        .btn-secondary {
            background: transparent;
            border: 2px solid #3498db;
        }
        .btn-secondary:hover {
            background: #3498db;
        }
        .content {
            padding: 50px 0;
            flex-grow: 1;
        }
        .card {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .form-group {
            margin-bottom: 1.5rem;
        }
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #2c3e50;
        }
        .form-control {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e1e1;
            border-radius: 5px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        .form-control:focus {
            outline: none;
            border-color: #3498db;
        }
        .messages {
            margin: 20px 0;
        }
        .alert {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-top: auto;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <nav class="nav">
                <div class="logo">🔧 UAP Campus Fixer</div>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    {% if user.is_authenticated %}
                        <li><a href="/dashboard">Dashboard</a></li>
                        <li><a href="/report-issue">Report Issue</a></li>
                        <li><a href="/track-issue">Track Issue</a></li>
                        <li><a href="/logout">Logout ({{ user.username }})</a></li>
                    {% else %}
                        <li><a href="/register">Register</a></li>
                        <li><a href="/login">Login</a></li>
                    {% endif %}
                </ul>
            </nav>
        </div>
    </header>

    <main>
        {% if messages %}
        <div class="container messages">
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% block content %}
        {% endblock %}
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 UAP Campus Fixer. Simplifying Campus Maintenance.</p>
        </div>
    </footer>
</body>
</html>'''

    with open('campus_fixer/templates/campus_fixer/base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)
    print("✅ base.html created")

    # 6. Create index.html
    index_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
<section class="hero">
    <div class="container">
        <h1>UAP Campus Fixer</h1>
        <p>Simplifying Campus Maintenance Requests</p>
        <p>Campus Fixer provides a powerful, intuitive platform to streamline the entire maintenance request process.</p>
        <div style="margin-top: 2rem;">
            {% if user.is_authenticated %}
                <a href="/dashboard" class="btn">Go to Dashboard</a>
                <a href="/report-issue" class="btn btn-secondary">Report Issue</a>
            {% else %}
                <a href="/register" class="btn">Get Started</a>
                <a href="/login" class="btn btn-secondary">Login</a>
            {% endif %}
        </div>
    </div>
</section>

<div class="content">
    <div class="container">
        <div class="card">
            <h2 style="text-align: center; margin-bottom: 2rem;">Our Objectives</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
                <div style="text-align: center; padding: 1.5rem;">
                    <h3>🚀 User-Friendly</h3>
                    <p>Easy issue reporting for everyone</p>
                </div>
                <div style="text-align: center; padding: 1.5rem;">
                    <h3>💬 Communication</h3>
                    <p>Better coordination with maintenance teams</p>
                </div>
                <div style="text-align: center; padding: 1.5rem;">
                    <h3>⏰ Fast Resolution</h3>
                    <p>Quick response and resolution times</p>
                </div>
                <div style="text-align: center; padding: 1.5rem;">
                    <h3>📊 Reduce Downtime</h3>
                    <p>Minimize campus disruptions</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

    with open('campus_fixer/templates/campus_fixer/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("✅ index.html created")

    # 7. Create register.html
    register_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Register{% endblock %}

{% block content %}
<div class="content">
    <div class="container">
        <div class="card" style="max-width: 500px; margin: 0 auto;">
            <h2 style="text-align: center; margin-bottom: 2rem;">Create Account</h2>
            
            <form method="post">
                {% csrf_token %}
                
                {% if form.errors %}
                <div class="alert alert-error">
                    Please correct the errors below.
                </div>
                {% endif %}
                
                <div class="form-group">
                    <label for="id_username">Username:</label>
                    <input type="text" name="username" id="id_username" class="form-control" required 
                           value="{{ form.username.value|default:'' }}">
                    {% if form.username.errors %}
                    <div style="color: #e74c3c; font-size: 0.9rem; margin-top: 0.5rem;">
                        {{ form.username.errors }}
                    </div>
                    {% endif %}
                </div>
                
                <div class="form-group">
                    <label for="id_password1">Password:</label>
                    <input type="password" name="password1" id="id_password1" class="form-control" required>
                    {% if form.password1.errors %}
                    <div style="color: #e74c3c; font-size: 0.9rem; margin-top: 0.5rem;">
                        {{ form.password1.errors }}
                    </div>
                    {% endif %}
                </div>
                
                <div class="form-group">
                    <label for="id_password2">Confirm Password:</label>
                    <input type="password" name="password2" id="id_password2" class="form-control" required>
                    {% if form.password2.errors %}
                    <div style="color: #e74c3c; font-size: 0.9rem; margin-top: 0.5rem;">
                        {{ form.password2.errors }}
                    </div>
                    {% endif %}
                </div>
                
                <button type="submit" class="btn" style="width: 100%; padding: 15px; font-size: 1.1rem;">
                    Create Account
                </button>
            </form>
            
            <p style="text-align: center; margin-top: 1.5rem;">
                Already have an account? <a href="/login" style="color: #3498db;">Login here</a>
            </p>
        </div>
    </div>
</div>
{% endblock %}'''

    with open('campus_fixer/templates/campus_fixer/register.html', 'w', encoding='utf-8') as f:
        f.write(register_html)
    print("✅ register.html created")

    # 8. Create login.html
    login_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="content">
    <div class="container">
        <div class="card" style="max-width: 500px; margin: 0 auto;">
            <h2 style="text-align: center; margin-bottom: 2rem;">Login</h2>
            
            <form method="post">
                {% csrf_token %}
                
                {% if form.errors %}
                <div class="alert alert-error">
                    Invalid username or password.
                </div>
                {% endif %}
                
                <div class="form-group">
                    <label for="id_username">Username:</label>
                    <input type="text" name="username" id="id_username" class="form-control" required 
                           value="{{ form.username.value|default:'' }}">
                </div>
                
                <div class="form-group">
                    <label for="id_password">Password:</label>
                    <input type="password" name="password" id="id_password" class="form-control" required>
                </div>
                
                <button type="submit" class="btn" style="width: 100%; padding: 15px; font-size: 1.1rem;">
                    Login
                </button>
            </form>
            
            <p style="text-align: center; margin-top: 1.5rem;">
                Don't have an account? <a href="/register" style="color: #3498db;">Register here</a>
            </p>
        </div>
    </div>
</div>
{% endblock %}'''

    with open('campus_fixer/templates/campus_fixer/login.html', 'w', encoding='utf-8') as f:
        f.write(login_html)
    print("✅ login.html created")

    # 9. Create dashboard.html
    dashboard_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="content">
    <div class="container">
        <div class="card">
            <h2>Welcome, {{ user.username }}! 👋</h2>
            <p>This is your dashboard. From here you can manage all your maintenance requests.</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 2rem;">
                <a href="/report-issue" class="btn" style="text-align: center; display: flex; flex-direction: column; align-items: center;">
                    <span style="font-size: 2rem; margin-bottom: 0.5rem;">📝</span>
                    Report New Issue
                </a>
                <a href="/track-issue" class="btn btn-secondary" style="text-align: center; display: flex; flex-direction: column; align-items: center;">
                    <span style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</span>
                    Track Issues
                </a>
            </div>
        </div>
        
        <div class="card">
            <h3>Quick Stats</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1rem;">
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 5px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #3498db;">0</div>
                    <div>Issues Reported</div>
                </div>
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 5px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #f39c12;">0</div>
                    <div>In Progress</div>
                </div>
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 5px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #27ae60;">0</div>
                    <div>Resolved</div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

    with open('campus_fixer/templates/campus_fixer/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    print("✅ dashboard.html created")

    # 10. Create other pages
    simple_pages = {
        'report_issue.html': 'Report Issue',
        'track_issue.html': 'Track Issue', 
        'admin_dashboard.html': 'Admin Dashboard'
    }

    for page, title in simple_pages.items():
        content = f'''{{% extends 'campus_fixer/base.html' %}}

{{% block title %}}{title}{{% endblock %}}

{{% block content %}}
<div class="content">
    <div class="container">
        <div class="card">
            <h2>{title}</h2>
            <p>This page is under development. Functionality will be added soon.</p>
            <a href="/dashboard" class="btn">Back to Dashboard</a>
        </div>
    </div>
</div>
{{% endblock %}}'''
        
        with open(f'campus_fixer/templates/campus_fixer/{page}', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {page} created")

def main():
    print("🚀 COMPLETE UAP CAMPUS FIXER FIX")
    print("=" * 60)
    
    create_files()
    
    print("\n🔄 Running migrations...")
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")
    
    print("\n" + "=" * 60)
    print("🎉 FIX COMPLETED SUCCESSFULLY!")
    print("\n🚀 Now run these commands:")
    print("1. python manage.py runserver")
    print("2. Open http://127.0.0.1:8000/")
    print("\n📝 Test these pages:")
    print("   - http://127.0.0.1:8000/register/")
    print("   - http://127.0.0.1:8000/login/")
    print("   - http://127.0.0.1:8000/dashboard/")
    print("\n✅ All pages should now work properly!")

if __name__ == "__main__":
    main()
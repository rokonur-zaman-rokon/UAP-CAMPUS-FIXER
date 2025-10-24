import os
import sys
from datetime import datetime, timezone
import subprocess
from pathlib import Path
from colorama import Fore, Style, init

# ✅ Initialize color output for terminal (cross-platform)
init(autoreset=True)

# Small helper for colorful, readable console messages
def smart_print(icon, message, color=Fore.WHITE):
    print(f"{color}{icon} {message}{Style.RESET_ALL}")

def final_complete_fix():
    # 🕒 Show current UTC time — useful for debugging or logs
    now_utc = datetime.now(timezone.utc)
    smart_print("🕒", f"Current UTC time: {now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}", Fore.CYAN)
    
    smart_print("🚀", "APPLYING FINAL COMPLETE FIX", Fore.GREEN)
    print("=" * 70)

    # 🗂 Define key directories
    base_dir = Path(__file__).resolve().parent
    app_dir = base_dir / "campus_fixer"
    app_dir.mkdir(exist_ok=True)  # Create the app folder if it doesn’t exist

    # 📦 Files to auto-generate — full Django app core
    files = {
        # -------------------- forms.py --------------------
        "forms.py": '''from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Issue, UserProfile

# ✅ Custom user creation form to include profile info
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES)
    department = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        # ✅ We only include core User model fields here
        fields = ('username','email','password1','password2')

    def save(self, commit=True):
        # ✅ Overriding save() to create a linked UserProfile
        user = super().save(commit)
        UserProfile.objects.create(
            user=user,
            user_type=self.cleaned_data['user_type'],
            department=self.cleaned_data['department'],
            phone_number=self.cleaned_data['phone_number']
        )
        return user

# ✅ Form to submit issues
class IssueForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Issue
        fields = ['anonymous','user_type','department','category','location','description']
        # ✅ Using Textarea for longer text fields for better UI
        widgets = {
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
        }
''',

        # -------------------- views.py --------------------
        "views.py": '''from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Issue
from .forms import IssueForm

# ✅ Home Page
def index(request):
    return render(request,'campus_fixer/index.html')

# ✅ User Registration Page
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, f"Account created for {user.username}!")
        return redirect('login')
    return render(request,'campus_fixer/register.html',{'form':form})

# ✅ Custom Login Page
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
    return render(request,'campus_fixer/login.html',{'form':form})

# ✅ Logout function with success message
def custom_logout(request):
    auth_logout(request)
    messages.success(request,'Logged out successfully!')
    return redirect('index')

# ✅ Dashboard showing recent issues
@login_required(login_url='/login/')
def dashboard(request):
    user_issues = Issue.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request,'campus_fixer/dashboard.html',{'user_issues':user_issues})
''',

        # -------------------- models.py --------------------
        "models.py": '''from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# ✅ Extended profile for users
class UserProfile(models.Model):
    USER_TYPES = [
        ('student','Student'),
        ('faculty','Faculty'),
        ('staff','Staff')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    department = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

# ✅ Core Issue model storing complaint/ticket data
class Issue(models.Model):
    ticket_id = models.CharField(max_length=36, unique=True, default=lambda: str(uuid.uuid4()))  # short unique ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=UserProfile.USER_TYPES)
    department = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.status}"

# ✅ Tracks updates or comments made on issues
class IssueUpdate(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='updates')
    update_text = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
''',

        # -------------------- admin.py --------------------
        "admin.py": '''from django.contrib import admin
from .models import UserProfile, Issue, IssueUpdate

# ✅ Admin customization for better visibility
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','user_type','department','phone_number')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('ticket_id','user','status','created_at')
    search_fields = ('ticket_id','description')

@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ('issue','updated_by','created_at')
''',

        # -------------------- urls.py --------------------
        "urls.py": '''from django.urls import path
from . import views

# ✅ URL routing table — keeps things simple and organized
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
''',

        # -------------------- test_imports.py --------------------
        "test_imports.py": '''import os, sys, django
from pathlib import Path

# ✅ Ensure the script finds Django project root
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','uap_campus_fixer.settings')

print("🔍 Checking Django setup...")
try:
    django.setup()
    # ✅ If all imports succeed, Django setup is healthy
    from campus_fixer.models import Issue, UserProfile, IssueUpdate
    from campus_fixer.forms import IssueForm
    from campus_fixer.views import index, dashboard
    print("✅ ALL IMPORTS WORKING PERFECTLY!")
except Exception as e:
    print(f"❌ Error during setup: {e}")
'''
    }

    # 🧠 Write all files safely using Pathlib
    for filename, content in files.items():
        file_path = app_dir / filename if filename != "test_imports.py" else base_dir / filename
        file_path.write_text(content, encoding="utf-8")
        smart_print("✅", f"{filename} created successfully", Fore.YELLOW)

    # 🕒 Log completion time
    smart_print("🕒", f"Fix completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Fore.CYAN)

    # 🧩 Test that Django imports and setup work
    smart_print("🧠", "Running import test...", Fore.MAGENTA)
    try:
        result = subprocess.run([sys.executable, str(base_dir / "test_imports.py")],
                                capture_output=True, text=True, check=True)
        print(result.stdout)
        smart_print("🎉", "Environment validation successful!", Fore.GREEN)
    except subprocess.CalledProcessError as e:
        smart_print("❌", "Test failed:", Fore.RED)
        print(e.stdout or "", e.stderr or "")

if __name__ == "__main__":
    final_complete_fix()

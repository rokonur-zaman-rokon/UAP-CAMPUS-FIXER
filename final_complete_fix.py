import os
import sys
from datetime import datetime, timezone
import subprocess

def final_complete_fix():
    # Get current UTC time
    now_utc = datetime.now(timezone.utc)
    print("🕒 Current UTC time:", now_utc.strftime("%Y-%m-%d %H:%M:%S UTC"))
    
    print("🚀 APPLYING FINAL COMPLETE FIX")
    print("=" * 60)


    files = {
        "forms.py": '''from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Issue, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES)
    department = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15, required=False)
    class Meta:
        model = User
        fields = ('username','email','password1','password2','user_type','department','phone_number')

class IssueForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, initial=False)
    class Meta:
        model = Issue
        fields = ['anonymous','user_type','department','category','location','description']
        widgets = {k: forms.TextInput(attrs={'class':'form-control'}) for k in ['location','description']}
''',

        "views.py": '''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as auth_logout
from .models import Issue, IssueUpdate
from .forms import IssueForm

def index(request): return render(request,'campus_fixer/index.html')
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method=="POST" and form.is_valid(): 
        user=form.save(); messages.success(request,f"Account created for {user.username}!"); return redirect('login')
    return render(request,'campus_fixer/register.html',{'form':form})
def custom_login(request):
    if request.user.is_authenticated: return redirect('dashboard')
    form=AuthenticationForm(request,data=request.POST or None)
    if request.method=="POST" and form.is_valid():
        user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if user: login(request,user); messages.success(request,f"Welcome back, {user.username}!"); return redirect('dashboard')
    return render(request,'campus_fixer/login.html',{'form':form})
def custom_logout(request): auth_logout(request); messages.success(request,'Logged out'); return redirect('index')
@login_required(login_url='/login/')
def dashboard(request):
    user_issues=Issue.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request,'campus_fixer/dashboard.html',{'user_issues':user_issues})
''',

        "models.py": '''from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class UserProfile(models.Model):
    USER_TYPES=[('student','Student'),('faculty','Faculty'),('staff','Staff')]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_type=models.CharField(max_length=10,choices=USER_TYPES)
    department=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15,blank=True)
class Issue(models.Model):
    ticket_id=models.CharField(max_length=20,unique=True,default=uuid.uuid4)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    anonymous=models.BooleanField(default=False)
    user_type=models.CharField(max_length=10,choices=UserProfile.USER_TYPES)
    department=models.CharField(max_length=20)
    category=models.CharField(max_length=20)
    location=models.CharField(max_length=200)
    description=models.TextField()
    status=models.CharField(max_length=20,default='pending')
    created_at=models.DateTimeField(default=timezone.now)
    updated_at=models.DateTimeField(auto_now=True)
class IssueUpdate(models.Model):
    issue=models.ForeignKey(Issue,on_delete=models.CASCADE,related_name='updates')
    update_text=models.TextField()
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(default=timezone.now)
''',

        "admin.py": '''from django.contrib import admin
from .models import UserProfile, Issue, IssueUpdate
admin.site.register(UserProfile)
admin.site.register(Issue)
admin.site.register(IssueUpdate)
''',

        "urls.py": '''from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.custom_login,name='login'),
    path('logout/',views.custom_logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
]
''',

        "test_imports.py": '''import os, sys, django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','uap_campus_fixer.settings')
try:
    django.setup()
    from campus_fixer.models import Issue, UserProfile, IssueUpdate
    from campus_fixer.forms import IssueForm
    from campus_fixer.views import index, dashboard
    print("✅ ALL IMPORTS WORKING!")
except Exception as e:
    print(f"❌ Error: {e}")
'''
    }

    os.makedirs("campus_fixer", exist_ok=True)
    for filename, content in files.items():
        with open(f"campus_fixer/{filename}" if filename!="test_imports.py" else filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ {filename} created")

    print("🕒 Fix completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Run test imports
    try:
        result = subprocess.run([sys.executable,"test_imports.py"],capture_output=True,text=True,check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Test failed:\n",e.stdout,e.stderr)

if __name__=="__main__":
    final_complete_fix()

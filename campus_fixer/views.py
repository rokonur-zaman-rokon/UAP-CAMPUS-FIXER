from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Issue, UserProfile

def index(request):
    return render(request, 'campus_fixer/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created for {username}! Welcome to Campus Fixer!')
                return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'campus_fixer/register.html', {'form': form})

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
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

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('index')

@login_required
def dashboard(request):
    return render(request, 'campus_fixer/dashboard.html')

@login_required
def report_issue(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        priority = request.POST.get('priority')
        building = request.POST.get('building')
        location = request.POST.get('location')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Fetch user's profile info
        profile = UserProfile.objects.filter(user=request.user).first()
        user_type = profile.user_type if profile else 'student'
        department = profile.department if profile else 'OTHERS'

        Issue.objects.create(
            user=request.user,
            user_type=user_type,
            department=department,
            category=category,
            location=location,
            description=description,
            image=image
        )

        messages.success(request, 'Issue reported successfully! Your ticket has been created.')
        return redirect('dashboard')
    
    return render(request, 'campus_fixer/report_issue.html')

@login_required
def track_issue(request):
    issues = Issue.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'campus_fixer/track_issue.html', {'issues': issues})

from django.shortcuts import render, redirect, get_object_or_404
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
    total_issues = Issue.objects.count()
    pending_issues = Issue.objects.filter(status='pending').count()
    in_progress_issues = Issue.objects.filter(status='in_progress').count()
    resolved_issues = Issue.objects.filter(status='resolved').count()
    closed_issues = Issue.objects.filter(status='closed').count()
    urgent_issues = Issue.objects.filter(priority='urgent').count() if hasattr(Issue, 'priority') else 0

    recent_issues = Issue.objects.order_by('-created_at')[:5]

    context = {
        'total_issues': total_issues,
        'pending_issues': pending_issues,
        'in_progress_issues': in_progress_issues,
        'resolved_issues': resolved_issues,
        'closed_issues': closed_issues,
        'urgent_issues': urgent_issues,
        'recent_issues': recent_issues,
    }
    return render(request, 'campus_fixer/dashboard.html', context)


@login_required
def report_issue(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        location = request.POST.get('location')
        description = request.POST.get('description')
        image = request.FILES.get('image')

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


@login_required
def update_issue(request, ticket_id):
    issue = get_object_or_404(Issue, ticket_id=ticket_id, user=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        issue.status = new_status
        issue.save()
        messages.success(request, f"Issue {issue.ticket_id} status updated successfully!")
        return redirect('track_issue')

    return render(request, 'campus_fixer/update_issue.html', {'issue': issue})

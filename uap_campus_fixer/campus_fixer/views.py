from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Issue, UserProfile, IssueUpdate, Feedback
from .forms import CustomUserCreationForm, IssueForm, FeedbackForm

def index(request):
    return render(request, 'campus_fixer/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type'],
                department=form.cleaned_data['department'],
                phone_number=form.cleaned_data['phone_number']
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'campus_fixer/register.html', {'form': form})

@login_required
def dashboard(request):
    user_issues = Issue.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'campus_fixer/dashboard.html', {'issues': user_issues})

@login_required
def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            
            # Create initial update
            IssueUpdate.objects.create(
                issue=issue,
                update_text=f"Issue reported. Status: {issue.status}",
                updated_by=request.user
            )
            
            messages.success(request, f'Issue reported successfully! Ticket ID: {issue.ticket_id}')
            return redirect('dashboard')
    else:
        form = IssueForm()
    return render(request, 'campus_fixer/report_issue.html', {'form': form})

@login_required
def track_issue(request, ticket_id=None):
    if ticket_id:
        issue = get_object_or_404(Issue, ticket_id=ticket_id, user=request.user)
        return render(request, 'campus_fixer/track_issue.html', {'issue': issue})
    
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        try:
            issue = Issue.objects.get(ticket_id=ticket_id, user=request.user)
            return redirect('track_issue', ticket_id=ticket_id)
        except Issue.DoesNotExist:
            messages.error(request, 'Issue not found or you do not have permission to view it.')
    
    return render(request, 'campus_fixer/track_issue.html')

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    issues = Issue.objects.all().order_by('-created_at')
    pending_count = Issue.objects.filter(status='pending').count()
    in_progress_count = Issue.objects.filter(status='in_progress').count()
    
    context = {
        'issues': issues,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
    }
    return render(request, 'campus_fixer/admin_dashboard.html', context)

@login_required
def issue_detail(request, ticket_id):
    issue = get_object_or_404(Issue, ticket_id=ticket_id)
    
    # Check if user has permission to view this issue
    if issue.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this issue.')
        return redirect('dashboard')
    
    if request.method == 'POST' and request.user.is_staff:
        new_status = request.POST.get('status')
        update_text = request.POST.get('update_text')
        
        if new_status and new_status != issue.status:
            issue.status = new_status
            issue.save()
            
            IssueUpdate.objects.create(
                issue=issue,
                update_text=f"Status changed to {new_status}. {update_text}",
                updated_by=request.user
            )
            messages.success(request, 'Issue status updated successfully!')
    
    updates = issue.updates.all().order_by('-created_at')
    return render(request, 'campus_fixer/issue_detail.html', {
        'issue': issue,
        'updates': updates
    })

@login_required
def add_feedback(request, ticket_id):
    issue = get_object_or_404(Issue, ticket_id=ticket_id, user=request.user)
    
    if issue.status != 'resolved':
        messages.error(request, 'You can only provide feedback for resolved issues.')
        return redirect('dashboard')
    
    if hasattr(issue, 'feedback'):
        messages.error(request, 'Feedback already provided for this issue.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.issue = issue
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('dashboard')
    else:
        form = FeedbackForm()
    
    return render(request, 'campus_fixer/add_feedback.html', {'form': form, 'issue': issue})
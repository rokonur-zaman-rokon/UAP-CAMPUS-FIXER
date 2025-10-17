import os

def fix_forms_issue():
    print("🚀 FIXING FORMS.PY ISSUE")
    print("=" * 50)
    
    # 1. Create the complete forms.py file
    print("📋 Creating complete forms.py...")
    forms_content = '''from django import forms
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
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'department', 'phone_number')

class IssueForm(forms.ModelForm):
    anonymous = forms.BooleanField(
        required=False, 
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Issue
        fields = ['anonymous', 'user_type', 'department', 'category', 'location', 'description']
        widgets = {
            'user_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'department': forms.Select(attrs={
                'class': 'form-control', 
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Building, floor, room number',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the issue in detail...',
                'required': True
            }),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
'''

    with open('campus_fixer/forms.py', 'w', encoding='utf-8') as f:
        f.write(forms_content)
    print("✅ forms.py created with IssueForm")

    # 2. Update views.py to handle the forms properly
    print("👁️ Updating views.py...")
    views_content = '''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as auth_logout
from .models import Issue, UserProfile, IssueUpdate
from .forms import IssueForm

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
    """Custom logout view - works with GET"""
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, 'You have been successfully logged out.')
    return redirect('index')

@login_required(login_url='/login/')
def dashboard(request):
    """User dashboard"""
    # Get user's issues
    user_issues = Issue.objects.filter(user=request.user).order_by('-created_at')[:5]
    total_issues = Issue.objects.filter(user=request.user).count()
    pending_issues = Issue.objects.filter(user=request.user, status='pending').count()
    resolved_issues = Issue.objects.filter(user=request.user, status='resolved').count()
    
    context = {
        'user_issues': user_issues,
        'total_issues': total_issues,
        'pending_issues': pending_issues,
        'resolved_issues': resolved_issues,
    }
    return render(request, 'campus_fixer/dashboard.html', context)

@login_required(login_url='/login/')
def report_issue(request):
    """Report issue page"""
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            
            # Generate ticket ID
            import uuid
            issue.ticket_id = f"UAP{str(uuid.uuid4())[:8].upper()}"
            
            issue.save()
            
            # Create initial update
            IssueUpdate.objects.create(
                issue=issue,
                update_text=f"Issue reported successfully. Status: {issue.status}",
                updated_by=request.user
            )
            
            messages.success(request, f'Issue reported successfully! Your Ticket ID: {issue.ticket_id}')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = IssueForm()
    
    return render(request, 'campus_fixer/report_issue.html', {'form': form})

@login_required(login_url='/login/')
def track_issue(request, ticket_id=None):
    """Track issue page"""
    if ticket_id:
        # Single issue view
        issue = get_object_or_404(Issue, ticket_id=ticket_id, user=request.user)
        updates = issue.updates.all().order_by('-created_at')
        return render(request, 'campus_fixer/track_issue.html', {
            'issue': issue, 
            'updates': updates,
            'ticket_id': ticket_id
        })
    
    # All issues view
    user_issues = Issue.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        search_ticket_id = request.POST.get('ticket_id', '').strip()
        if search_ticket_id:
            try:
                issue = Issue.objects.get(ticket_id=search_ticket_id.upper(), user=request.user)
                return redirect('track_issue_detail', ticket_id=search_ticket_id.upper())
            except Issue.DoesNotExist:
                messages.error(request, f'Issue with Ticket ID "{search_ticket_id}" not found.')
    
    return render(request, 'campus_fixer/track_issue.html', {
        'user_issues': user_issues,
        'ticket_id': None
    })

@login_required(login_url='/login/')
def admin_dashboard(request):
    """Admin dashboard"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    all_issues = Issue.objects.all().order_by('-created_at')
    pending_count = Issue.objects.filter(status='pending').count()
    in_progress_count = Issue.objects.filter(status='in_progress').count()
    resolved_count = Issue.objects.filter(status='resolved').count()
    
    context = {
        'all_issues': all_issues,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
    }
    return render(request, 'campus_fixer/admin_dashboard.html', context)

@login_required(login_url='/login/')
def issue_detail(request, ticket_id):
    """Issue detail view"""
    issue = get_object_or_404(Issue, ticket_id=ticket_id)
    
    # Check if user has permission to view this issue
    if issue.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this issue.')
        return redirect('dashboard')
    
    updates = issue.updates.all().order_by('-created_at')
    
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
    
    return render(request, 'campus_fixer/issue_detail.html', {
        'issue': issue,
        'updates': updates
    })
'''

    with open('campus_fixer/views.py', 'w', encoding='utf-8') as f:
        f.write(views_content)
    print("✅ views.py updated")

    # 3. Update models.py to ensure all models exist
    print("🗃️ Ensuring models.py is complete...")
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = f"UAP{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.ticket_id} - {self.category}"

class IssueUpdate(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='updates')
    update_text = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Update for {self.issue.ticket_id}"

class Feedback(models.Model):
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Feedback for {self.issue.ticket_id} - Rating: {self.rating}"
'''

    with open('campus_fixer/models.py', 'w', encoding='utf-8') as f:
        f.write(models_content)
    print("✅ models.py updated")

    # 4. Update admin.py to register all models
    print("⚙️ Updating admin.py...")
    admin_content = '''from django.contrib import admin
from .models import UserProfile, Issue, IssueUpdate, Feedback

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'department']
    list_filter = ['user_type', 'department']
    search_fields = ['user__username']

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'category', 'department', 'status', 'created_at']
    list_filter = ['status', 'category', 'department', 'created_at']
    search_fields = ['ticket_id', 'user__username', 'description', 'location']
    readonly_fields = ['ticket_id', 'created_at']

@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ['issue', 'updated_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['issue__ticket_id', 'update_text']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['issue', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['issue__ticket_id', 'comment']
'''

    with open('campus_fixer/admin.py', 'w', encoding='utf-8') as f:
        f.write(admin_content)
    print("✅ admin.py updated")

    # 5. Update report_issue.html to use the form properly
    print("📝 Updating report_issue.html...")
    report_issue_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Report Issue{% endblock %}

{% block content %}
<div class="content">
    <div class="container">
        <div class="card">
            <h2 style="text-align: center; margin-bottom: 2rem; color: #2c3e50;">
                <i class="fas fa-plus-circle" style="color: #3498db; margin-right: 10px;"></i>
                Report an Issue
            </h2>
            
            {% if messages %}
            <div class="messages">
                {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    <i class="fas fa-{% if message.tags == 'success' %}check-circle{% else %}exclamation-triangle{% endif %}" style="margin-right: 10px;"></i>
                    {{ message }}
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <form method="post">
                {% csrf_token %}
                
                {% if form.errors %}
                <div class="alert alert-error">
                    <i class="fas fa-exclamation-triangle" style="margin-right: 10px;"></i>
                    <strong>Please correct the following errors:</strong>
                    <ul style="margin: 10px 0 0 20px;">
                        {% for field in form %}
                            {% for error in field.errors %}
                                <li>{{ field.label }}: {{ error }}</li>
                            {% endfor %}
                        {% endfor %}
                        {% for error in form.non_field_errors %}
                            <li>{{ error }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
                
                <!-- Anonymous Reporting -->
                <div class="form-group" style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
                    <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: 500;">
                        {{ form.anonymous }}
                        <span>Report this issue anonymously</span>
                    </label>
                    <small style="color: #666; margin-left: 28px; display: block; margin-top: 5px;">
                        <i class="fas fa-user-secret" style="margin-right: 5px;"></i>
                        Your identity will be hidden from public view
                    </small>
                </div>
                
                <!-- User Type -->
                <div class="form-group">
                    <label for="id_user_type">
                        <i class="fas fa-user-tag" style="color: #3498db; margin-right: 8px;"></i>
                        Who is reporting the issue? *
                    </label>
                    {{ form.user_type }}
                </div>
                
                <!-- Department -->
                <div class="form-group">
                    <label for="id_department">
                        <i class="fas fa-building" style="color: #3498db; margin-right: 8px;"></i>
                        Select Department *
                    </label>
                    {{ form.department }}
                </div>
                
                <!-- Category -->
                <div class="form-group">
                    <label for="id_category">
                        <i class="fas fa-tag" style="color: #3498db; margin-right: 8px;"></i>
                        Select Category *
                    </label>
                    {{ form.category }}
                </div>
                
                <!-- Location -->
                <div class="form-group">
                    <label for="id_location">
                        <i class="fas fa-map-marker-alt" style="color: #3498db; margin-right: 8px;"></i>
                        Location *
                    </label>
                    {{ form.location }}
                </div>
                
                <!-- Description -->
                <div class="form-group">
                    <label for="id_description">
                        <i class="fas fa-file-alt" style="color: #3498db; margin-right: 8px;"></i>
                        Description *
                    </label>
                    {{ form.description }}
                </div>
                
                <!-- Submit Button -->
                <button type="submit" class="btn" style="width: 100%; padding: 15px; font-size: 1.1rem; background: linear-gradient(135deg, #27ae60, #229954);">
                    <i class="fas fa-paper-plane" style="margin-right: 10px;"></i>
                    Submit Issue Report
                </button>
            </form>
            
            <!-- Tips Section -->
            <div style="margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px;">
                <h4 style="margin-bottom: 1rem; display: flex; align-items: center;">
                    <i class="fas fa-lightbulb" style="margin-right: 10px;"></i>
                    Tips for Better Issue Reporting
                </h4>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Be specific about the exact location (building, floor, room number)</li>
                    <li>Provide clear and detailed description of the problem</li>
                    <li>Mention how the issue is affecting you or others</li>
                    <li>Include any safety concerns if applicable</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<style>
    .form-control {
        width: 100%;
        padding: 12px;
        border: 2px solid #e1e1e1;
        border-radius: 8px;
        font-size: 1rem;
        transition: all 0.3s;
        background: white;
    }
    
    .form-control:focus {
        outline: none;
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    select.form-control {
        appearance: none;
        background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
        background-repeat: no-repeat;
        background-position: right 12px center;
        background-size: 16px;
        padding-right: 40px;
    }
    
    textarea.form-control {
        resize: vertical;
        min-height: 120px;
    }
    
    .form-check-input {
        width: 20px;
        height: 20px;
        margin-right: 10px;
    }
    
    .alert ul {
        margin: 10px 0 0 0;
    }
    
    .alert li {
        margin-bottom: 5px;
    }
</style>
{% endblock %}'''

    with open('campus_fixer/templates/campus_fixer/report_issue.html', 'w', encoding='utf-8') as f:
        f.write(report_issue_html)
    print("✅ report_issue.html updated")

def main():
    print("🚀 APPLYING COMPLETE FORMS FIX...")
    print("=" * 60)
    
    fix_forms_issue()
    
    print("\n" + "=" * 60)
    print("🎉 FORMS FIX COMPLETED SUCCESSFULLY!")
    print("\n🔄 Now run these commands:")
    print("python manage.py makemigrations")
    print("python manage.py migrate")
    print("python manage.py runserver")
    print("\n✅ The IssueForm import error should be fixed now!")

if __name__ == "__main__":
    main()
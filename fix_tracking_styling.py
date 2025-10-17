import os

def fix_tracking_and_styling():
    print("🎨 FIXING TRACKING & STYLING ISSUES")
    print("=" * 60)
    
    # 1. First, let's update views.py to ensure proper data passing
    print("👁️ Updating views.py for better data handling...")
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
        form = IssueForm(request.POST, request.FILES)
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

    # 2. Create professional-looking track_issue.html
    print("📊 Creating professional track_issue.html...")
    track_issue_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Track Issue{% endblock %}

{% block content %}
<div class="content">
    <div class="container">
        {% if ticket_id %}
            <!-- Single Issue Tracking View -->
            <div class="card">
                <div class="card-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid #f1f1f1;">
                    <h2 style="margin: 0; color: #2c3e50;">
                        <i class="fas fa-ticket-alt" style="color: #3498db; margin-right: 10px;"></i>
                        Track Issue: <span style="color: #e74c3c;">{{ issue.ticket_id }}</span>
                    </h2>
                    <span class="status-badge status-{{ issue.status }}" style="padding: 0.7rem 1.5rem; border-radius: 25px; font-weight: bold; font-size: 1rem;">
                        <i class="fas fa-{% if issue.status == 'resolved' %}check-circle{% elif issue.status == 'in_progress' %}sync-alt{% else %}clock{% endif %}" style="margin-right: 8px;"></i>
                        {{ issue.status|title }}
                    </span>
                </div>
                
                <!-- Issue Details Grid -->
                <div class="details-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
                    <div class="detail-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px;">
                        <div style="font-size: 0.9rem; opacity: 0.9;">CATEGORY</div>
                        <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">
                            <i class="fas fa-tag" style="margin-right: 8px;"></i>
                            {{ issue.get_category_display }}
                        </div>
                    </div>
                    
                    <div class="detail-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1.5rem; border-radius: 10px;">
                        <div style="font-size: 0.9rem; opacity: 0.9;">DEPARTMENT</div>
                        <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">
                            <i class="fas fa-building" style="margin-right: 8px;"></i>
                            {{ issue.get_department_display }}
                        </div>
                    </div>
                    
                    <div class="detail-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 1.5rem; border-radius: 10px;">
                        <div style="font-size: 0.9rem; opacity: 0.9;">LOCATION</div>
                        <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">
                            <i class="fas fa-map-marker-alt" style="margin-right: 8px;"></i>
                            {{ issue.location }}
                        </div>
                    </div>
                    
                    <div class="detail-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 1.5rem; border-radius: 10px;">
                        <div style="font-size: 0.9rem; opacity: 0.9;">REPORTED DATE</div>
                        <div style="font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;">
                            <i class="fas fa-calendar-alt" style="margin-right: 8px;"></i>
                            {{ issue.created_at|date:"M d, Y" }}
                        </div>
                    </div>
                </div>
                
                <!-- Description Section -->
                <div class="description-section" style="background: #f8f9fa; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
                    <h3 style="color: #2c3e50; margin-bottom: 1rem; display: flex; align-items: center;">
                        <i class="fas fa-file-alt" style="color: #3498db; margin-right: 10px;"></i>
                        Issue Description
                    </h3>
                    <p style="margin: 0; color: #555; line-height: 1.6; font-size: 1.1rem;">{{ issue.description }}</p>
                </div>
                
                <!-- Status Updates Timeline -->
                <div class="timeline-section">
                    <h3 style="color: #2c3e50; margin-bottom: 2rem; display: flex; align-items: center;">
                        <i class="fas fa-history" style="color: #3498db; margin-right: 10px;"></i>
                        Status Updates Timeline
                    </h3>
                    
                    <div class="timeline" style="position: relative;">
                        {% for update in updates %}
                        <div class="timeline-item" style="display: flex; margin-bottom: 2rem; position: relative;">
                            <div class="timeline-marker" style="width: 20px; height: 20px; background: #3498db; border-radius: 50%; margin-right: 1.5rem; flex-shrink: 0; position: relative; z-index: 2;"></div>
                            <div class="timeline-content" style="flex: 1; background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 3px 15px rgba(0,0,0,0.1); border-left: 4px solid #3498db;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                    <strong style="color: #2c3e50; font-size: 1.1rem;">
                                        <i class="fas fa-user" style="color: #7f8c8d; margin-right: 8px;"></i>
                                        {{ update.updated_by.username }}
                                    </strong>
                                    <small style="color: #95a5a6; font-size: 0.9rem;">
                                        <i class="fas fa-clock" style="margin-right: 5px;"></i>
                                        {{ update.created_at|date:"M d, Y H:i" }}
                                    </small>
                                </div>
                                <p style="margin: 0; color: #34495e; line-height: 1.5;">{{ update.update_text }}</p>
                            </div>
                        </div>
                        {% empty %}
                        <div style="text-align: center; padding: 3rem; color: #7f8c8d;">
                            <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                            <h4>No updates yet</h4>
                            <p>Your issue is currently under review. Updates will appear here.</p>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <!-- Action Buttons -->
                <div style="display: flex; gap: 1rem; margin-top: 2rem; justify-content: center;">
                    <a href="{% url 'track_issue' %}" class="btn btn-secondary" style="display: flex; align-items: center;">
                        <i class="fas fa-arrow-left" style="margin-right: 8px;"></i>
                        Back to All Issues
                    </a>
                    <a href="{% url 'report_issue' %}" class="btn" style="display: flex; align-items; center; background: #27ae60;">
                        <i class="fas fa-plus" style="margin-right: 8px;"></i>
                        Report New Issue
                    </a>
                </div>
            </div>
            
        {% else %}
            <!-- All Issues View -->
            <div class="card">
                <div class="card-header" style="text-align: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid #f1f1f1;">
                    <h2 style="color: #2c3e50; margin: 0;">
                        <i class="fas fa-search" style="color: #3498db; margin-right: 10px;"></i>
                        Track Your Issues
                    </h2>
                    <p style="color: #7f8c8d; margin: 0.5rem 0 0 0;">Monitor the status of your reported issues</p>
                </div>
                
                {% if messages %}
                <div class="messages">
                    {% for message in messages %}
                    <div class="alert alert-{{ message.tags }}" style="margin-bottom: 2rem;">
                        <i class="fas fa-{% if message.tags == 'success' %}check-circle{% else %}exclamation-triangle{% endif %}" style="margin-right: 10px;"></i>
                        {{ message }}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                
                <!-- Search Section -->
                <div class="search-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
                    <h4 style="color: white; margin-bottom: 1rem; display: flex; align-items: center;">
                        <i class="fas fa-search" style="margin-right: 10px;"></i>
                        Search by Ticket ID
                    </h4>
                    <form method="post" style="display: flex; gap: 1rem;">
                        {% csrf_token %}
                        <input type="text" name="ticket_id" placeholder="Enter Ticket ID (e.g., UAP12345678)" 
                               class="form-control" style="flex: 1; padding: 1rem; font-size: 1rem;" required
                               pattern="UAP[A-Z0-9]{8}" title="Please enter a valid Ticket ID (e.g., UAP12345678)">
                        <button type="submit" class="btn" style="background: rgba(255,255,255,0.2); border: 2px solid white; padding: 1rem 2rem;">
                            <i class="fas fa-search" style="margin-right: 8px;"></i>
                            Search
                        </button>
                    </form>
                </div>
                
                <!-- Issues List -->
                <div class="issues-section">
                    <h3 style="color: #2c3e50; margin-bottom: 1.5rem; display: flex; align-items: center;">
                        <i class="fas fa-list" style="color: #3498db; margin-right: 10px;"></i>
                        Your Reported Issues
                    </h3>
                    
                    {% if user_issues %}
                        <div class="issues-grid" style="display: grid; gap: 1.5rem;">
                            {% for issue in user_issues %}
                            <div class="issue-card" style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 3px 15px rgba(0,0,0,0.1); border-left: 5px solid 
                                        {% if issue.status == 'resolved' %}#27ae60
                                        {% elif issue.status == 'in_progress' %}#f39c12
                                        {% else %}#3498db{% endif %}; 
                                        transition: transform 0.3s, box-shadow 0.3s;">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                                    <div style="flex: 1;">
                                        <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50; font-size: 1.3rem;">
                                            <i class="fas fa-{% if issue.category == 'electrical' %}bolt{% elif issue.category == 'plumbing' %}faucet{% elif issue.category == 'cleanliness' %}broom{% else %}tools{% endif %}" 
                                               style="color: #3498db; margin-right: 10px;"></i>
                                            {{ issue.get_category_display }}
                                        </h4>
                                        <div style="color: #7f8c8d; font-size: 0.9rem; margin-bottom: 0.5rem;">
                                            <strong style="color: #e74c3c;">Ticket ID: {{ issue.ticket_id }}</strong> • 
                                            Department: {{ issue.get_department_display }} • 
                                            Location: {{ issue.location }}
                                        </div>
                                        <p style="margin: 0; color: #555; line-height: 1.4;">
                                            {{ issue.description|truncatewords:25 }}
                                        </p>
                                    </div>
                                    <div style="text-align: right; min-width: 150px;">
                                        <span class="status-badge status-{{ issue.status }}" 
                                              style="padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold; font-size: 0.9rem; display: inline-block; margin-bottom: 0.5rem;">
                                            <i class="fas fa-{% if issue.status == 'resolved' %}check-circle{% elif issue.status == 'in_progress' %}sync-alt{% else %}clock{% endif %}" 
                                               style="margin-right: 5px;"></i>
                                            {{ issue.status|title }}
                                        </span>
                                        <div>
                                            <a href="{% url 'track_issue_detail' issue.ticket_id %}" class="btn" style="padding: 0.5rem 1rem; font-size: 0.9rem; display: inline-flex; align-items: center;">
                                                <i class="fas fa-eye" style="margin-right: 5px;"></i>
                                                View Details
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #ecf0f1; display: flex; justify-content: space-between; align-items: center; color: #95a5a6; font-size: 0.85rem;">
                                    <span>
                                        <i class="fas fa-calendar" style="margin-right: 5px;"></i>
                                        Reported on {{ issue.created_at|date:"M d, Y" }}
                                        {% if issue.anonymous %}
                                        <span style="background: #bdc3c7; color: white; padding: 0.2rem 0.5rem; border-radius: 10px; margin-left: 0.5rem; font-size: 0.7rem;">
                                            <i class="fas fa-user-secret" style="margin-right: 3px;"></i>Anonymous
                                        </span>
                                        {% endif %}
                                    </span>
                                    <span>
                                        <i class="fas fa-history" style="margin-right: 5px;"></i>
                                        Last update: {{ issue.updated_at|date:"M d, Y" }}
                                    </span>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div style="text-align: center; padding: 4rem; color: #7f8c8d;">
                            <i class="fas fa-inbox" style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                            <h3 style="color: #95a5a6; margin-bottom: 1rem;">No Issues Reported Yet</h3>
                            <p style="margin-bottom: 2rem; font-size: 1.1rem;">You haven't reported any issues yet. Start by reporting your first maintenance issue!</p>
                            <a href="{% url 'report_issue' %}" class="btn" style="padding: 1rem 2rem; font-size: 1.1rem; display: inline-flex; align-items: center;">
                                <i class="fas fa-plus" style="margin-right: 8px;"></i>
                                Report Your First Issue
                            </a>
                        </div>
                    {% endif %}
                </div>
            </div>
        {% endif %}
    </div>
</div>

<style>
    .status-badge {
        text-transform: capitalize;
        color: white;
    }
    
    .status-pending {
        background: linear-gradient(135deg, #3498db, #2980b9);
    }
    
    .status-in_progress {
        background: linear-gradient(135deg, #f39c12, #e67e22);
    }
    
    .status-resolved {
        background: linear-gradient(135deg, #27ae60, #229954);
    }
    
    .status-closed {
        background: linear-gradient(135deg, #7f8c8d, #95a5a6);
    }
    
    .issue-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 25px rgba(0,0,0,0.15);
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 10px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: #ecf0f1;
        z-index: 1;
    }
    
    @media (max-width: 768px) {
        .details-grid {
            grid-template-columns: 1fr;
        }
        
        .search-section form {
            flex-direction: column;
        }
        
        .issue-card > div {
            flex-direction: column;
        }
        
        .issue-card > div > div:last-child {
            text-align: left;
            margin-top: 1rem;
        }
    }
</style>

<!-- Add Font Awesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
{% endblock %}'''

    with open('campus_fixer/templates/campus_fixer/track_issue.html', 'w', encoding='utf-8') as f:
        f.write(track_issue_html)
    print("✅ Professional track_issue.html created")

    # 3. Update base.html to include Font Awesome
    print("🎨 Updating base.html with Font Awesome...")
    try:
        with open('campus_fixer/templates/campus_fixer/base.html', 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        # Add Font Awesome CDN if not present
        if 'font-awesome' not in base_content and 'fontawesome' not in base_content:
            # Add in head section
            head_end = base_content.find('</head>')
            if head_end != -1:
                font_awesome_link = '\n    <!-- Font Awesome Icons -->\n    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'
                base_content = base_content[:head_end] + font_awesome_link + base_content[head_end:]
        
        with open('campus_fixer/templates/campus_fixer/base.html', 'w', encoding='utf-8') as f:
            f.write(base_content)
        print("✅ base.html updated with Font Awesome")
    except Exception as e:
        print(f"⚠️ Could not update base.html: {e}")

def main():
    print("🚀 APPLYING TRACKING & STYLING FIX...")
    print("=" * 60)
    
    fix_tracking_and_styling()
    
    print("\n" + "=" * 60)
    print("🎉 TRACKING & STYLING FIX COMPLETED!")
    print("\n🚀 Now test these features:")
    print("   1. Report a new issue - should generate Ticket ID")
    print("   2. Go to Track Issues - should show beautiful interface")
    print("   3. Click View Details - should show professional timeline")
    print("   4. Search by Ticket ID - should work properly")
    print("\n✅ Tracking should now work with professional styling!")

if __name__ == "__main__":
    main()
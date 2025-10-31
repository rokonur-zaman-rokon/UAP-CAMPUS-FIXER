from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Issue, UserProfile, LostFoundComment
import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from campus_fixer.models import Issue

# ---------------------- HOME ----------------------
def index(request):
    issues_resolved = Issue.objects.filter(status='resolved').count()
    context = {'issues_resolved': issues_resolved}
    return render(request, 'campus_fixer/index.html', context)

# ---------------------- REGISTER ----------------------
def register(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not re.match(r"^[a-zA-Z0-9._%+-]+@uap-bd\.edu$", email):
            messages.error(request, "Only UAP email allowed (example: student@uap-bd.edu)")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered!")
            return redirect('register')

        username = email.split("@")[0]
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        UserProfile.objects.get_or_create(user=user)

        login(request, user)
        messages.success(request, "Account created successfully! Welcome 🎉")
        return redirect('index')  # Redirect to home after registration

    return render(request, 'campus_fixer/register.html')


# ---------------------- LOGIN ----------------------
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('index')  # Redirect authenticated users to home

    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not re.match(r"^[a-zA-Z0-9._%+-]+@uap-bd\.edu$", email):
            messages.error(request, "Enter valid UAP email (example: student@uap-bd.edu)")
            return redirect('login')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect('login')

        user = authenticate(request, username=user_obj.username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! ✅")
            return redirect('index')  # Redirect to home instead of dashboard
        else:
            messages.error(request, "Incorrect password ❌")
            return redirect('login')

    return render(request, 'campus_fixer/login.html')


# ---------------------- LOGOUT ----------------------
def custom_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully ✅")
    return redirect('index')


# ---------------------- DASHBOARD ----------------------
@login_required
def dashboard(request):
    total_issues = Issue.objects.count()
    pending_issues = Issue.objects.filter(status='pending').count()
    in_progress_issues = Issue.objects.filter(status='in_progress').count()
    resolved_issues = Issue.objects.filter(status='resolved').count()
    closed_issues = Issue.objects.filter(status='closed').count()
    urgent_issues = Issue.objects.filter(priority='urgent').count()
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


# ---------------------- REPORT ISSUE ----------------------
@login_required
def report_issue(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        location = request.POST.get('location')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        building = request.POST.get('building')
        department = request.POST.get('department')
        image = request.FILES.get('image')


        is_emergency = True if request.POST.get('is_emergency') == 'on' else False

        profile = UserProfile.objects.filter(user=request.user).first()
        user_type = profile.user_type if profile else 'student'

        Issue.objects.create(
            user=request.user,
            user_type=user_type,
            department=department,
            category=category,
            priority=priority,
            building=building,
            location=location,
            description=description,
            image=image,
            is_emergency=is_emergency
            
        )

        messages.success(request, "Issue reported successfully ✅")
        return redirect('dashboard')

    return render(request, 'campus_fixer/report_issue.html')


# ---------------------- TRACK ISSUES ----------------------
@login_required
def track_issue(request):
    issues = Issue.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'campus_fixer/track_issue.html', {'issues': issues})


# ---------------------- UPDATE STATUS ----------------------
@login_required
def update_issue(request, ticket_id):
    issue = get_object_or_404(Issue, ticket_id=ticket_id, user=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        issue.status = new_status
        issue.save()
        messages.success(request, "Status updated ✅")
        return redirect('track_issue')

    return render(request, 'campus_fixer/update_issue.html', {'issue': issue})


# ---------------------- LOST & FOUND FEED ----------------------
@login_required
def lost_found_feed(request):
    choice = request.GET.get('type')  # 'report' or 'found'

    if request.method == "POST":
        # --- Comment Submission ---
        if 'comment_text' in request.POST:
            post_id = request.POST.get("post_id")
            comment_text = request.POST.get("comment_text")
            post = get_object_or_404(Issue, id=post_id)
            LostFoundComment.objects.create(post=post, user=request.user, comment_text=comment_text)
            messages.success(request, "Comment added ✅")
            return redirect(f"{request.path}?type=found")

        # --- Lost/Found Report Submission ---
        status = request.POST.get('status')
        department = request.POST.get('department')
        location = request.POST.get('location')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if status not in ['lost', 'found']:
            messages.error(request, "Please select Lost or Found ❗")
            return redirect(f"{request.path}?type=report")

        Issue.objects.create(
            user=request.user,
            category='lost_found',
            status=status,
            department=department,
            location=location,
            description=description,
            image=image
        )
        messages.success(request, f"{status.capitalize()} item reported successfully ✅")
        return redirect('lost_found_feed')

    # --- Display Found Items ---
    found_posts = None
    if choice == 'found':
        found_posts = Issue.objects.filter(category='lost_found', status='found').order_by('-created_at')

    context = {
        'choice': choice,
        'found_posts': found_posts
    }
    return render(request, 'campus_fixer/lost_found_feed.html', context)


# ---------------------- REAL-TIME RESOLVED COUNT ----------------------
def issues_resolved_count(request):
    resolved_count = Issue.objects.filter(status='resolved').count()
    return JsonResponse({'resolved_count': resolved_count})

#custom admin dashboard
@login_required
def admin_dashboard(request):
    context = {
        'total_issues': Issue.objects.count(),
        'pending_count': Issue.objects.filter(status='pending').count(),
        'in_progress_count': Issue.objects.filter(status='in_progress').count(),
        'resolved_count': Issue.objects.filter(status='resolved').count(),
        'all_issues': Issue.objects.order_by('-created_at')[:10],
    }
    return render(request, 'campus_fixer/admin_dashboard.html', context)

def track_issue_detail(request, ticket_id):
    issue = get_object_or_404(Issue, ticket_id=ticket_id)
    return render(request, 'campus_fixer/track_issue_detail.html', {'issue': issue})
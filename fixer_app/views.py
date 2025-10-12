from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, IssueForm
from .models import Issue, Profile

def front_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'front_page.html')


# Home / dashboard
def home(request):
    if request.user.is_authenticated:
        issues = Issue.objects.all()
        return render(request, 'home.html', {'issues': issues})
    return redirect('signup')

from django.contrib.auth import authenticate, login as auth_login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'front_page.html', {'error': 'Invalid credentials'})
    return render(request, 'front_page.html')


# User signup
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, user_type='student')  # default, can add selection later
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# Report a new issue
def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            if not form.cleaned_data['anonymous']:
                issue.reporter = request.user.profile
            issue.save()
            return redirect('home')
    else:
        form = IssueForm()
    return render(request, 'report_issue.html', {'form': form})


# View issue details
def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    return render(request, 'issue_detail.html', {'issue': issue})


# Update issue status (for maintenance team)
def update_issue(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IssueForm(instance=issue)
    return render(request, 'report_issue.html', {'form': form})

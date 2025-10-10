from django import forms
from .models import Issue
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# User registration form
class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Issue reporting form
class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'location', 'priority', 'anonymous']

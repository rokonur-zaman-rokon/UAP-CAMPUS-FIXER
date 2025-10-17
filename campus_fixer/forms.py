from django import forms
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

import os

def fix_admin_imports():
    print("🚀 FIXING ADMIN.PY IMPORT ISSUES")
    print("=" * 50)
    
    # First, let's check what's actually in models.py
    print("📋 Checking current models.py...")
    try:
        with open('campus_fixer/models.py', 'r', encoding='utf-8') as f:
            models_content = f.read()
        print("✅ models.py exists")
        
        # Check which models are defined
        models_defined = []
        if 'class UserProfile' in models_content:
            models_defined.append('UserProfile')
        if 'class Issue' in models_content:
            models_defined.append('Issue') 
        if 'class IssueUpdate' in models_content:
            models_defined.append('IssueUpdate')
        if 'class Feedback' in models_content:
            models_defined.append('Feedback')
            
        print(f"📊 Models found: {models_defined}")
        
    except FileNotFoundError:
        print("❌ models.py not found")
        return
    
    # Now create admin.py that only imports what exists
    print("⚙️ Creating correct admin.py...")
    
    admin_imports = "from django.contrib import admin\n"
    admin_classes = ""
    
    if 'UserProfile' in models_defined:
        admin_imports += "from .models import UserProfile\n"
        admin_classes += '''
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'department']
    list_filter = ['user_type', 'department']
    search_fields = ['user__username']
'''
    
    if 'Issue' in models_defined:
        admin_imports += "from .models import Issue\n"
        admin_classes += '''
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'category', 'department', 'status', 'created_at']
    list_filter = ['status', 'category', 'department', 'created_at']
    search_fields = ['ticket_id', 'user__username', 'description', 'location']
    readonly_fields = ['ticket_id', 'created_at']
'''
    
    if 'IssueUpdate' in models_defined:
        admin_imports += "from .models import IssueUpdate\n"
        admin_classes += '''
@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ['issue', 'updated_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['issue__ticket_id', 'update_text']
'''
    
    if 'Feedback' in models_defined:
        admin_imports += "from .models import Feedback\n"
        admin_classes += '''
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['issue', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['issue__ticket_id', 'comment']
'''
    
    admin_content = admin_imports + admin_classes
    
    with open('campus_fixer/admin.py', 'w', encoding='utf-8') as f:
        f.write(admin_content)
    print("✅ admin.py created with correct imports")

def create_complete_models():
    print("🗃️ Creating complete models.py...")
    
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
    # Temporarily commented out to avoid Pillow issues
    # image = models.ImageField(upload_to='issues/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
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
    print("✅ Complete models.py created")

def main():
    print("🚀 APPLYING COMPLETE FIX FOR ADMIN IMPORTS")
    print("=" * 60)
    
    # First create complete models
    create_complete_models()
    
    # Then fix admin imports
    fix_admin_imports()
    
    print("\n" + "=" * 60)
    print("🎉 COMPLETE FIX APPLIED!")
    print("\n🔄 Now run these commands:")
    print("python manage.py makemigrations")
    print("python manage.py migrate")
    print("python manage.py runserver")
    print("\n✅ All import issues should be resolved now!")

if __name__ == "__main__":
    main()
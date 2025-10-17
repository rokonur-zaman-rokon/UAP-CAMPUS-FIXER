import os

def create_simple_models():
    print("🚀 CREATING SIMPLE MODELS (NO IMAGEFIELD)")
    print("=" * 50)
    
    # Create models without ImageField to avoid Pillow issues
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
    # Removed ImageField temporarily
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
    print("✅ Simple models.py created (no ImageField)")

def main():
    print("🚀 APPLYING SIMPLE MODELS FIX...")
    print("=" * 50)
    
    create_simple_models()
    
    print("\n🔄 Now run these commands:")
    print("python manage.py makemigrations")
    print("python manage.py migrate")
    print("python manage.py runserver")
    print("\n✅ This should work without Pillow errors!")

if __name__ == "__main__":
    main()
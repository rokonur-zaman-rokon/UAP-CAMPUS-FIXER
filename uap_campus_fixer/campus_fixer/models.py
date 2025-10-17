from django.db import models
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
        ('CSE', 'Computer Science & Engineering'),
        ('EEE', 'Electrical & Electronic Engineering'),
        ('ARCHITECTURE', 'Architecture'),
        ('CIVIL', 'Civil Engineering'),
        ('BBA', 'Business Administration'),
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
        ('suggestions', 'Suggestions & Improvements'),
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
    image = models.ImageField(upload_to='issues/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    
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
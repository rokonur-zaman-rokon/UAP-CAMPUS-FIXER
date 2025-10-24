from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# ---------------------- USER PROFILE ----------------------
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


# ---------------------- ISSUE ----------------------
def generate_ticket_id():
    return f"UAP{str(uuid.uuid4())[:8].upper()}"


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

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    BUILDING_CHOICES = [
        ('academic', 'Academic Building'),
        ('library', 'Library'),
        ('hostel', 'RH Home Center'),
        ('cafeteria', 'Cafeteria'),
        ('sports', 'Gaming Room'),
        ('admin', 'Administrative Building'),
    ]
    
    ticket_id = models.CharField(max_length=20, unique=True, default=generate_ticket_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=UserProfile.USER_TYPES)
    department = models.CharField(max_length=20, choices=DEPARTMENTS)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    building = models.CharField(max_length=50, choices=BUILDING_CHOICES, default='academic')
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='issues/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.ticket_id} - {self.category}"


# ---------------------- ISSUE UPDATES ----------------------
class IssueUpdate(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='updates')
    update_text = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Update for {self.issue.ticket_id}"

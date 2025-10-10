from django.db import models
from django.contrib.auth.models import User

# Profile to differentiate student/staff/faculty
class Profile(models.Model):
    USER_TYPE = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('faculty', 'Faculty'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


# Reported issues
class Issue(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Normal', 'Normal'),
        ('High', 'High'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    reporter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"


# Maintenance team
class MaintenanceTeam(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

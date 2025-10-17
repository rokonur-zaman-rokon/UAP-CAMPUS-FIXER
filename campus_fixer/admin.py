from django.contrib import admin
from .models import UserProfile, Issue, IssueUpdate

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'department']

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'category', 'department', 'status', 'created_at']

@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ['issue', 'updated_by', 'created_at']

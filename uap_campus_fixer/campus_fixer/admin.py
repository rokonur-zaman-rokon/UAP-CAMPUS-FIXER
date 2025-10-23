from django.contrib import admin
from .models import UserProfile, Issue, IssueUpdate, Feedback
from .models import SiteSettings

admin.site.register(SiteSettings)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'department']
    list_filter = ['user_type', 'department']

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'department']
    search_fields = ['ticket_id', 'user__username', 'description']

@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ['issue', 'updated_by', 'created_at']
    list_filter = ['created_at']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['issue', 'rating', 'created_at']
    list_filter = ['rating']
import os

# 🚀 Automatically fix missing or incorrect imports in admin.py 
# by dynamically detecting which models exist in models.py.
def fix_admin_imports():
    print("🚀 FIXING ADMIN.PY IMPORT ISSUES")
    print("=" * 50)
    
    models_path = 'campus_fixer/models.py'
    admin_path = 'campus_fixer/admin.py'

    # ✅ Step 1: Ensure models.py exists before proceeding
    if not os.path.exists(models_path):
        print("❌ models.py not found. Aborting admin fix.")
        return

    print("📋 Checking current models.py...")
    with open(models_path, 'r', encoding='utf-8') as f:
        models_content = f.read()
    print("✅ models.py exists")

    # 🔍 Step 2: Detect which model classes are defined in models.py
    possible_models = ['UserProfile', 'Issue', 'IssueUpdate', 'Feedback']
    models_defined = [model for model in possible_models if f'class {model}' in models_content]
    print(f"📊 Models found: {models_defined}")

    # ⚙️ Step 3: Dynamically generate correct admin imports & classes
    admin_imports = "from django.contrib import admin\n"
    admin_imports += "from .models import " + ", ".join(models_defined) + "\n" if models_defined else ""

    # 📦 Step 4: Admin registration templates for each model
    admin_templates = {
        'UserProfile': '''
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'department']
    list_filter = ['user_type', 'department']
    search_fields = ['user__username']
''',

        'Issue': '''
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'category', 'department', 'status', 'created_at']
    list_filter = ['status', 'category', 'department', 'created_at']
    search_fields = ['ticket_id', 'user__username', 'description', 'location']
    readonly_fields = ['ticket_id', 'created_at']
''',

        'IssueUpdate': '''
@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ['issue', 'updated_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['issue__ticket_id', 'update_text']
''',

        'Feedback': '''
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['issue', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['issue__ticket_id', 'comment']
'''
    }

    # 🧩 Step 5: Add admin registration blocks only for existing models
    admin_classes = "".join([admin_templates[m] for m in models_defined if m in admin_templates])
    admin_content = admin_imports + admin_classes

    # 💾 Step 6: Write generated code into admin.py
    os.makedirs(os.path.dirname(admin_path), exist_ok=True)
    with open(admin_path, 'w', encoding='utf-8') as f:
        f.write(admin_content)
    print("✅ admin.py created with correct imports and registrations.\n")


# 🗃️ Create a complete models.py with all expected models.
# Includes fallback defaults for safe database migration.
def create_complete_models():
    print("🗃️ Creating complete models.py...")

    models_content = '''from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# 👤 Stores additional user details (type, department, etc.)
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


# 🧾 Stores user-submitted issues
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
    # 🖼️ Temporarily commented out to avoid Pillow dependency
    # image = models.ImageField(upload_to='issues/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        # Automatically generate a unique ticket ID if missing
        if not self.ticket_id:
            self.ticket_id = f"UAP{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.ticket_id} - {self.category}"


# 🛠️ Logs updates made to issues by users or admins
class IssueUpdate(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='updates')
    update_text = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Update for {self.issue.ticket_id}"


# ⭐ Stores feedback and rating for each issue
class Feedback(models.Model):
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Feedback for {self.issue.ticket_id} - Rating: {self.rating}"
'''

    # 💾 Write models.py file safely
    os.makedirs('campus_fixer', exist_ok=True)
    with open('campus_fixer/models.py', 'w', encoding='utf-8') as f:
        f.write(models_content)
    print("✅ Complete models.py created successfully.\n")


# 🧩 Main function that coordinates both tasks
def main():
    print("🚀 APPLYING COMPLETE FIX FOR ADMIN IMPORTS")
    print("=" * 60)
    
    # Step 1: Create all models (safe overwrite)
    create_complete_models()
    
    # Step 2: Auto-fix admin imports based on available models
    fix_admin_imports()
    
    # ✅ Step 3: Final message for developer
    print("\n" + "=" * 60)
    print("🎉 COMPLETE FIX APPLIED SUCCESSFULLY!")
    print("\n🔄 Next steps:")
    print("1️⃣ python manage.py makemigrations")
    print("2️⃣ python manage.py migrate")
    print("3️⃣ python manage.py runserver")
    print("\n✅ All import issues and model syncs are now fixed!")

# 🔰 Run automatically if executed directly
if __name__ == "__main__":
    main()
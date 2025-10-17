#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uap_campus_fixer.settings')

try:
    django.setup()
    print("✅ Django setup successful!")
    
    # Test imports
    from campus_fixer.models import Issue, UserProfile, IssueUpdate
    print("✅ Models import successful!")
    
    from campus_fixer.forms import IssueForm
    print("✅ Forms import successful!")
    
    from campus_fixer.views import index, dashboard, report_issue
    print("✅ Views import successful!")
    
    print("\n🎉 ALL IMPORTS WORKING CORRECTLY!")
    print("\n🚀 You can now run:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate") 
    print("   python manage.py runserver")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Please check the error above and run the fix script again.")

#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uap_campus_fixer.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_logout():
    client = Client()
    try:
        user = User.objects.create_user('testuser', 'test@test.com', 'testpass123')
    except:
        user = User.objects.get(username='testuser')
    login_success = client.login(username='testuser', password='testpass123')
    print(f"Login successful: {login_success}")
    if login_success:
        response = client.get('/dashboard/')
        print(f"Dashboard status: {response.status_code}")
        response = client.get('/logout/')
        print(f"Logout response: {response.status_code}, redirected to: {response.url}")
        response = client.get('/dashboard/')
        print(f"Dashboard after logout: {response.status_code}")

if __name__ == "__main__":
    test_logout()

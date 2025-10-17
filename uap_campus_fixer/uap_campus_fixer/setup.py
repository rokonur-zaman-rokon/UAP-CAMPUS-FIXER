#!/usr/bin/env python
import os
import sys
import subprocess
import platform

def run_command(command, shell=True):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, check=True, capture_output=True, text=True)
        print(f"✅ Success: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {command}")
        print(f"   Error: {e.stderr}")
        return False

def create_file(path, content):
    """Create a file with given content"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create {path}: {e}")
        return False

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run(["python", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ Python found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Python not found. Please install Python 3.8+ from python.org")
        return False

def setup_project():
    print("🚀 Setting up UAP Campus Fixer - Windows Edition")
    print("=" * 60)
    
    # Check Python
    if not check_python():
        return False
    
    # Create virtual environment
    print("\n📦 Creating virtual environment...")
    if not run_command("python -m venv uap_env"):
        print("❌ Failed to create virtual environment")
        return False
    
    # Windows-specific paths
    pip_path = "uap_env\\Scripts\\pip"
    python_path = "uap_env\\Scripts\\python"
    
    # Install dependencies
    print("\n📥 Installing dependencies...")
    
    # Create requirements.txt
    requirements_content = """Django>=4.2,<5.0
Pillow>=9.0,<10.0
"""
    create_file("requirements.txt", requirements_content)
    
    # Upgrade pip first
    print("🔄 Upgrading pip...")
    run_command(f'"{python_path}" -m pip install --upgrade pip')
    
    # Install dependencies
    print("📦 Installing Django and Pillow...")
    if not run_command(f'"{pip_path}" install -r requirements.txt'):
        print("❌ Failed to install dependencies")
        return False
    
    # Create necessary directories
    print("\n📁 Creating project structure...")
    directories = [
        "campus_fixer/templates/campus_fixer",
        "campus_fixer/static/campus_fixer/css", 
        "campus_fixer/static/campus_fixer/js",
        "campus_fixer/static/campus_fixer/images",
        "media/issues"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ Created: {directory}")
    
    # Create sample CSS file
    print("\n🎨 Creating sample files...")
    css_content = """:root {
    --primary: #2c3e50;
    --secondary: #3498db;
    --accent: #e74c3c;
    --light: #ecf0f1;
    --dark: #2c3e50;
    --success: #27ae60;
    --warning: #f39c12;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.header {
    background: var(--primary);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo i {
    font-size: 2rem;
    color: var(--secondary);
}

.hero {
    background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('/static/campus_fixer/images/campus-bg.jpg');
    background-size: cover;
    background-position: center;
    color: white;
    padding: 100px 0;
    text-align: center;
}

.btn {
    display: inline-block;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
}

.btn-primary {
    background: var(--secondary);
    color: white;
}

.btn-primary:hover {
    background: #2980b9;
}

.card {
    background: white;
    border-radius: 10px;
    padding: 2rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.form-control {
    width: 100%;
    padding: 12px;
    border: 2px solid #e1e1e1;
    border-radius: 5px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.form-control:focus {
    outline: none;
    border-color: var(--secondary);
}"""
    
    create_file("campus_fixer/static/campus_fixer/css/style.css", css_content)
    
    # Create placeholder image note
    create_file("campus_fixer/static/campus_fixer/images/README.txt", 
                "Add your campus background image here as 'campus-bg.jpg'")
    
    # Run migrations
    print("\n🗃️ Running database migrations...")
    if not run_command(f'"{python_path}" manage.py makemigrations'):
        print("⚠️ No migrations to create")
    
    if not run_command(f'"{python_path}" manage.py migrate'):
        print("❌ Failed to run migrations")
        return False
    
    # Collect static files
    print("\n📊 Collecting static files...")
    run_command(f'"{python_path}" manage.py collectstatic --noinput')
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("\n🎯 NEXT STEPS:")
    print("1. Activate virtual environment:")
    print("   uap_env\\Scripts\\activate")
    print("2. Start the development server:")
    print("   python manage.py runserver")
    print("3. Open your browser to: http://127.0.0.1:8000/")
    print("4. Create superuser (optional):")
    print("   python manage.py createsuperuser")
    print("\n📝 Admin URL: http://127.0.0.1:8000/admin/")
    print("🎨 Add your campus image to: campus_fixer/static/campus_fixer/images/campus-bg.jpg")
    print("\n🚀 Your UAP Campus Fixer is ready!")

if __name__ == "__main__":
    setup_project()
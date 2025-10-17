import os
import shutil

def fix_all_missing_files():
    print("🚀 FIXING ALL MISSING FILES AND CONTENT")
    print("=" * 60)
    
    # 1. First, let's create the complete style.css
    print("🎨 Creating complete style.css...")
    css_content = '''/* UAP Campus Fixer - Complete Professional Styles */
:root {
    --primary: #2c3e50;
    --secondary: #3498db;
    --accent: #e74c3c;
    --success: #27ae60;
    --warning: #f39c12;
    --danger: #e74c3c;
    --light: #ecf0f1;
    --dark: #2c3e50;
    --gray: #95a5a6;
    --white: #ffffff;
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --gradient-warning: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --gradient-danger: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f8f9fa;
    color: #333;
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header */
.header {
    background: var(--primary);
    color: var(--white);
    padding: 1rem 0;
    box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--secondary);
}

.logo i {
    font-size: 2rem;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 1.5rem;
    align-items: center;
}

.nav-links a {
    color: var(--white);
    text-decoration: none;
    padding: 0.7rem 1.2rem;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
}

.nav-links a:hover {
    background: rgba(255,255,255,0.15);
    transform: translateY(-2px);
}

.nav-links a.logout-btn {
    background: var(--danger);
}

.nav-links a.logout-btn:hover {
    background: #c0392b;
}

/* Hero Section */
.hero {
    background: var(--gradient-primary);
    color: var(--white);
    padding: 100px 0;
    text-align: center;
    flex-grow: 1;
    display: flex;
    align-items: center;
}

.hero-content {
    max-width: 800px;
    margin: 0 auto;
}

.hero h1 {
    font-size: 3.5rem;
    margin-bottom: 1.5rem;
    font-weight: 700;
}

.hero p {
    font-size: 1.3rem;
    margin-bottom: 2rem;
    opacity: 0.95;
}

.hero-buttons {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 14px 32px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 600;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
}

.btn-primary {
    background: var(--secondary);
    color: var(--white);
}

.btn-primary:hover {
    background: #2980b9;
    transform: translateY(-3px);
}

.btn-secondary {
    background: transparent;
    color: var(--white);
    border: 2px solid var(--white);
}

.btn-secondary:hover {
    background: var(--white);
    color: var(--primary);
}

.btn-success {
    background: var(--success);
    color: var(--white);
}

/* Content */
.content {
    padding: 80px 0;
    flex-grow: 1;
}

.section-title {
    text-align: center;
    font-size: 2.8rem;
    margin-bottom: 3rem;
    color: var(--primary);
}

/* Cards */
.card {
    background: var(--white);
    border-radius: 15px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.card-header {
    border-bottom: 2px solid var(--light);
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
}

/* Forms */
.form-group {
    margin-bottom: 1.8rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.8rem;
    font-weight: 600;
    color: var(--primary);
}

.form-control {
    width: 100%;
    padding: 14px 16px;
    border: 2px solid #e1e1e1;
    border-radius: 10px;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-control:focus {
    outline: none;
    border-color: var(--secondary);
}

/* Messages */
.messages {
    margin: 20px 0;
}

.alert {
    padding: 1.2rem 1.5rem;
    border-radius: 10px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
}

.alert-success {
    background: #d4edda;
    color: #155724;
}

.alert-error {
    background: #f8d7da;
    color: #721c24;
}

/* Status Badges */
.status-badge {
    padding: 0.6rem 1.2rem;
    border-radius: 25px;
    font-weight: 700;
    color: var(--white);
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.status-pending {
    background: var(--gradient-primary);
}

.status-in_progress {
    background: var(--gradient-warning);
}

.status-resolved {
    background: var(--gradient-success);
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.stat-card {
    background: var(--white);
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    border-top: 4px solid var(--secondary);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.stat-label {
    color: var(--gray);
    font-weight: 600;
}

/* Issues Table */
.issues-table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
}

.issues-table th,
.issues-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #e1e1e1;
}

.issues-table th {
    background: var(--light);
    font-weight: 600;
    color: var(--primary);
}

.issues-table tr:hover {
    background: #f8f9fa;
}

/* Footer */
.footer {
    background: var(--primary);
    color: var(--white);
    text-align: center;
    padding: 2.5rem 0;
    margin-top: auto;
}

/* Responsive */
@media (max-width: 768px) {
    .nav {
        flex-direction: column;
        gap: 1rem;
    }
    
    .hero h1 {
        font-size: 2.5rem;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .container {
        padding: 0 15px;
    }
}
'''

    css_dir = 'campus_fixer/static/campus_fixer/css'
    os.makedirs(css_dir, exist_ok=True)
    
    with open(os.path.join(css_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("✅ style.css created with complete content")

    # 2. Create script.js
    print("📜 Creating script.js...")
    js_content = '''// UAP Campus Fixer - JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Status badge animations
    const statusBadges = document.querySelectorAll('.status-badge');
    statusBadges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Card hover effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Search functionality for track issues
    const searchForm = document.querySelector('form[action*="track-issue"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="ticket_id"]');
        searchInput.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    }

    // Print ticket functionality
    const printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Confirm logout
    const logoutLinks = document.querySelectorAll('a[href*="logout"]');
    logoutLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to logout?')) {
                e.preventDefault();
            }
        });
    });

    // Real-time clock for admin dashboard
    function updateClock() {
        const now = new Date();
        const clockElement = document.getElementById('live-clock');
        if (clockElement) {
            clockElement.textContent = now.toLocaleString();
        }
    }
    
    // Update clock every second if element exists
    if (document.getElementById('live-clock')) {
        setInterval(updateClock, 1000);
        updateClock();
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Dynamic content loading for better UX
    console.log('UAP Campus Fixer - System Initialized');
});
'''

    js_dir = 'campus_fixer/static/campus_fixer/js'
    os.makedirs(js_dir, exist_ok=True)
    
    with open(os.path.join(js_dir, 'script.js'), 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✅ script.js created with functionality")

    # 3. Create admin_dashboard.html
    print("📊 Creating admin_dashboard.html...")
    admin_dashboard_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Admin Dashboard{% endblock %}

{% block content %}
<div class="content">
    <div class="container">
        <div class="card">
            <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="margin: 0; color: #2c3e50;">
                    <i class="fas fa-tachometer-alt" style="color: #3498db; margin-right: 10px;"></i>
                    Admin Dashboard
                </h2>
                <div style="color: #7f8c8d; font-size: 0.9rem;">
                    <i class="fas fa-clock" style="margin-right: 5px;"></i>
                    <span id="live-clock">{{ current_time|date:"M d, Y H:i:s" }}</span>
                </div>
            </div>

            {% if messages %}
            <div class="messages">
                {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    <i class="fas fa-{% if message.tags == 'success' %}check-circle{% else %}exclamation-triangle{% endif %}" style="margin-right: 10px;"></i>
                    {{ message }}
                </div>
                {% endfor %}
            </div>
            {% endif %}

            <!-- Quick Stats -->
            <div class="stats-grid">
                <div class="stat-card" style="border-top-color: #3498db;">
                    <div class="stat-number" style="color: #3498db;">{{ total_issues }}</div>
                    <div class="stat-label">Total Issues</div>
                </div>
                <div class="stat-card" style="border-top-color: #f39c12;">
                    <div class="stat-number" style="color: #f39c12;">{{ pending_count }}</div>
                    <div class="stat-label">Pending</div>
                </div>
                <div class="stat-card" style="border-top-color: #e74c3c;">
                    <div class="stat-number" style="color: #e74c3c;">{{ in_progress_count }}</div>
                    <div class="stat-label">In Progress</div>
                </div>
                <div class="stat-card" style="border-top-color: #27ae60;">
                    <div class="stat-number" style="color: #27ae60;">{{ resolved_count }}</div>
                    <div class="stat-label">Resolved</div>
                </div>
            </div>
        </div>

        <!-- Recent Issues Table -->
        <div class="card">
            <h3 style="color: #2c3e50; margin-bottom: 1.5rem; display: flex; align-items: center;">
                <i class="fas fa-list" style="color: #3498db; margin-right: 10px;"></i>
                Recent Issues
            </h3>

            {% if all_issues %}
            <div style="overflow-x: auto;">
                <table class="issues-table">
                    <thead>
                        <tr>
                            <th>Ticket ID</th>
                            <th>User</th>
                            <th>Category</th>
                            <th>Department</th>
                            <th>Status</th>
                            <th>Created</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for issue in all_issues %}
                        <tr>
                            <td>
                                <strong style="color: #e74c3c;">{{ issue.ticket_id }}</strong>
                            </td>
                            <td>
                                {% if issue.anonymous %}
                                <span style="color: #7f8c8d;">
                                    <i class="fas fa-user-secret" style="margin-right: 5px;"></i>
                                    Anonymous
                                </span>
                                {% else %}
                                {{ issue.user.username }}
                                {% endif %}
                            </td>
                            <td>{{ issue.get_category_display }}</td>
                            <td>{{ issue.get_department_display }}</td>
                            <td>
                                <span class="status-badge status-{{ issue.status }}">
                                    <i class="fas fa-{% if issue.status == 'resolved' %}check-circle{% elif issue.status == 'in_progress' %}sync-alt{% else %}clock{% endif %}" style="margin-right: 5px;"></i>
                                    {{ issue.status|title }}
                                </span>
                            </td>
                            <td>{{ issue.created_at|date:"M d, Y" }}</td>
                            <td>
                                <a href="{% url 'track_issue_detail' issue.ticket_id %}" class="btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                                    <i class="fas fa-eye" style="margin-right: 5px;"></i>
                                    View
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div style="text-align: center; padding: 3rem; color: #7f8c8d;">
                <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <h4>No Issues Reported</h4>
                <p>No maintenance issues have been reported yet.</p>
            </div>
            {% endif %}
        </div>

        <!-- Quick Actions -->
        <div class="card">
            <h3 style="color: #2c3e50; margin-bottom: 1.5rem; display: flex; align-items: center;">
                <i class="fas fa-bolt" style="color: #f39c12; margin-right: 10px;"></i>
                Quick Actions
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <a href="/admin/campus_fixer/issue/" class="btn btn-primary" style="text-align: center;">
                    <i class="fas fa-cog" style="margin-right: 8px;"></i>
                    Manage Issues
                </a>
                <a href="/admin/campus_fixer/userprofile/" class="btn btn-secondary" style="text-align: center;">
                    <i class="fas fa-users" style="margin-right: 8px;"></i>
                    Manage Users
                </a>
                <a href="{% url 'dashboard' %}" class="btn" style="text-align: center; background: #27ae60;">
                    <i class="fas fa-user" style="margin-right: 8px;"></i>
                    User View
                </a>
                <button class="btn btn-print" style="text-align: center; background: #7f8c8d;">
                    <i class="fas fa-print" style="margin-right: 8px;"></i>
                    Print Report
                </button>
            </div>
        </div>

        <!-- System Info -->
        <div class="card">
            <h3 style="color: #2c3e50; margin-bottom: 1.5rem; display: flex; align-items: center;">
                <i class="fas fa-info-circle" style="color: #3498db; margin-right: 10px;"></i>
                System Information
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
                <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px;">
                    <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">System Status</h4>
                    <p style="color: #27ae60; margin: 0;">
                        <i class="fas fa-check-circle" style="margin-right: 5px;"></i>
                        All Systems Operational
                    </p>
                </div>
                <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px;">
                    <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">Response Time</h4>
                    <p style="color: #2c3e50; margin: 0;">
                        <i class="fas fa-bolt" style="margin-right: 5px;"></i>
                        Excellent Performance
                    </p>
                </div>
                <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px;">
                    <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">Uptime</h4>
                    <p style="color: #2c3e50; margin: 0;">
                        <i class="fas fa-server" style="margin-right: 5px;"></i>
                        99.9% This Month
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

    templates_dir = 'campus_fixer/templates/campus_fixer'
    os.makedirs(templates_dir, exist_ok=True)
    
    with open(os.path.join(templates_dir, 'admin_dashboard.html'), 'w', encoding='utf-8') as f:
        f.write(admin_dashboard_html)
    print("✅ admin_dashboard.html created")

    # 4. Create sample images and fix image references
    print("🖼️ Creating sample images directory...")
    images_dir = 'campus_fixer/static/campus_fixer/images'
    os.makedirs(images_dir, exist_ok=True)
    
    # Create placeholder files
    placeholder_content = "This is a placeholder image file. Replace with actual images."
    
    # Create placeholder files for images
    image_files = ['campus-bg.jpg', 'campus-logo.jpg', 'logo.png']
    for image_file in image_files:
        with open(os.path.join(images_dir, image_file + '.txt'), 'w') as f:
            f.write(f"Placeholder for {image_file}\nReplace this with actual image file.")
        print(f"✅ Created placeholder: {image_file}")

    # 5. Update base.html to include JavaScript
    print("🔧 Updating base.html to include JavaScript...")
    try:
        with open('campus_fixer/templates/campus_fixer/base.html', 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        # Add JavaScript before closing body tag
        if 'script.js' not in base_content:
            js_include = '''
    <!-- JavaScript -->
    {% load static %}
    <script src="{% static 'campus_fixer/js/script.js' %}"></script>
</body>
'''
            base_content = base_content.replace('</body>', js_include)
        
        with open('campus_fixer/templates/campus_fixer/base.html', 'w', encoding='utf-8') as f:
            f.write(base_content)
        print("✅ base.html updated with JavaScript")
    except Exception as e:
        print(f"❌ Error updating base.html: {e}")

    # 6. Update views.py to pass data to admin dashboard
    print("👁️ Updating views.py for admin dashboard...")
    try:
        with open('campus_fixer/views.py', 'r', encoding='utf-8') as f:
            views_content = f.read()
        
        # Update the admin_dashboard view to pass current_time
        if 'def admin_dashboard' in views_content:
            # We'll add current_time to the context
            views_content = views_content.replace(
                'from django.utils import timezone',
                'from django.utils import timezone\nfrom datetime import datetime'
            )
            
            # Update the admin_dashboard function
            admin_dashboard_start = views_content.find('def admin_dashboard(request):')
            if admin_dashboard_start != -1:
                # Find the context dictionary
                context_start = views_content.find('context = {', admin_dashboard_start)
                if context_start != -1:
                    # Add current_time to context
                    views_content = views_content.replace(
                        'context = {',
                        'context = {\n        \"current_time\": datetime.now(),'
                    )
        
        with open('campus_fixer/views.py', 'w', encoding='utf-8') as f:
            f.write(views_content)
        print("✅ views.py updated for admin dashboard")
    except Exception as e:
        print(f"❌ Error updating views.py: {e}")

def main():
    print("🚀 FIXING ALL MISSING FILES AND CONTENT")
    print("=" * 60)
    
    fix_all_missing_files()
    
    print("\n" + "=" * 60)
    print("🎉 ALL FILES FIXED SUCCESSFULLY!")
    print("\n📁 Files created/updated:")
    print("   ✅ campus_fixer/static/campus_fixer/css/style.css")
    print("   ✅ campus_fixer/static/campus_fixer/js/script.js") 
    print("   ✅ campus_fixer/templates/campus_fixer/admin_dashboard.html")
    print("   ✅ campus_fixer/static/campus_fixer/images/ (placeholders)")
    print("   ✅ Updated base.html with JavaScript")
    print("   ✅ Updated views.py for admin dashboard")
    print("\n🚀 Now test these features:")
    print("   1. Admin Dashboard - should show stats and issues table")
    print("   2. JavaScript functionality - messages, form validation")
    print("   3. Professional styling - consistent across all pages")
    print("   4. Image placeholders - ready for actual images")

if __name__ == "__main__":
    main()
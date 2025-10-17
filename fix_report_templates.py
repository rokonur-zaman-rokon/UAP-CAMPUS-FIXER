import os

def create_functional_templates():
    print("🚀 CREATING FUNCTIONAL REPORT & TRACK TEMPLATES")
    print("=" * 60)
    
    # 1. Create the actual report_issue.html template
    print("📝 Creating functional report_issue.html...")
    report_issue_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Report Issue{% endblock %}

{% block content %}
<div class="content">
    <div class="container">
        <div class="card">
            <h2 style="text-align: center; margin-bottom: 2rem; color: #2c3e50;">Report an Issue</h2>
            
            {% if messages %}
            <div class="messages">
                {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                {% if form.errors %}
                <div class="alert alert-error">
                    <strong>Please correct the following errors:</strong>
                    <ul>
                        {% for field in form %}
                            {% for error in field.errors %}
                                <li>{{ field.label }}: {{ error }}</li>
                            {% endfor %}
                        {% endfor %}
                        {% for error in form.non_field_errors %}
                            <li>{{ error }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
                
                <div class="form-group" style="background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 2rem;">
                    <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                        <input type="checkbox" name="anonymous" id="id_anonymous" class="form-control" style="width: auto;">
                        <span style="font-weight: 500;">Report this issue anonymously</span>
                    </label>
                    <small style="color: #666; margin-left: 28px;">Your identity will be hidden from public view</small>
                </div>
                
                <div class="form-group">
                    <label for="id_user_type">Who is reporting the issue? *</label>
                    <select name="user_type" id="id_user_type" class="form-control" required>
                        <option value="">Select User Type</option>
                        <option value="student">Student</option>
                        <option value="faculty">Faculty</option>
                        <option value="staff">Staff</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="id_department">Select Department *</label>
                    <select name="department" id="id_department" class="form-control" required>
                        <option value="">Select Department</option>
                        <option value="CSE">CSE</option>
                        <option value="EEE">EEE</option>
                        <option value="ARCHITECTURE">ARCHITECTURE</option>
                        <option value="CIVIL">CIVIL</option>
                        <option value="BBA">BBA</option>
                        <option value="ENGLISH">ENGLISH</option>
                        <option value="LAW">LAW</option>
                        <option value="PHARMACY">PHARMACY</option>
                        <option value="OTHERS">OTHERS</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="id_category">Select Category *</label>
                    <select name="category" id="id_category" class="form-control" required>
                        <option value="">Select Category</option>
                        <option value="electrical">Electrical</option>
                        <option value="plumbing">Plumbing</option>
                        <option value="cleanliness">Cleanliness</option>
                        <option value="it">IT</option>
                        <option value="furniture">Furniture</option>
                        <option value="safety">Safety</option>
                        <option value="lost_found">Lost & Found</option>
                        <option value="suggestions">Suggestions & Improvements</option>
                        <option value="others">Others</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="id_location">Location *</label>
                    <input type="text" name="location" id="id_location" class="form-control" 
                           placeholder="Building, floor, room number (e.g., Main Building, 2nd Floor, Room 205)" required>
                </div>
                
                <div class="form-group">
                    <label for="id_description">Description *</label>
                    <textarea name="description" id="id_description" class="form-control" rows="4" 
                              placeholder="Describe the issue in detail. Be specific about what needs to be fixed..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="id_image">Upload Photo (Optional)</label>
                    <input type="file" name="image" id="id_image" class="form-control" accept="image/*">
                    <small style="color: #666;">Upload a photo to help us understand the issue better</small>
                </div>
                
                <button type="submit" class="btn" style="width: 100%; padding: 15px; font-size: 1.1rem; background: #27ae60;">
                    📝 Submit Issue Report
                </button>
            </form>
            
            <div style="margin-top: 2rem; padding: 1rem; background: #e8f4fd; border-radius: 5px;">
                <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">💡 Tips for better issue reporting:</h4>
                <ul style="color: #666; margin: 0;">
                    <li>Be specific about the location</li>
                    <li>Provide clear details about the problem</li>
                    <li>Include photos when possible</li>
                    <li>Mention how the issue affects you</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<style>
    .form-checkbox {
        width: auto !important;
        margin-right: 10px;
    }
    
    .alert ul {
        margin: 0;
        padding-left: 20px;
    }
</style>
{% endblock %}'''

    with open('campus_fixer/templates/campus_fixer/report_issue.html', 'w', encoding='utf-8') as f:
        f.write(report_issue_html)
    print("✅ report_issue.html created")

    # 2. Create the actual track_issue.html template
    print("📊 Creating functional track_issue.html...")
    track_issue_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Track Issue{% endblock %}

{% block content %}
<div class="content">
    <div class="container">
        {% if ticket_id %}
            <!-- Single Issue Tracking View -->
            <div class="card">
                <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 1rem;">
                    <h2>Track Issue: {{ issue.ticket_id }}</h2>
                    <span class="status-badge status-{{ issue.status }}" style="padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
                        {{ issue.status|title }}
                    </span>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 5px;">
                        <strong>Category:</strong> {{ issue.get_category_display }}
                    </div>
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 5px;">
                        <strong>Department:</strong> {{ issue.get_department_display }}
                    </div>
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 5px;">
                        <strong>Location:</strong> {{ issue.location }}
                    </div>
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 5px;">
                        <strong>Reported:</strong> {{ issue.created_at|date:"M d, Y" }}
                    </div>
                </div>
                
                <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 5px; margin-bottom: 2rem;">
                    <strong>Description:</strong>
                    <p style="margin: 0.5rem 0 0 0; color: #666;">{{ issue.description }}</p>
                </div>
                
                {% if issue.image %}
                <div style="margin-bottom: 2rem;">
                    <strong>Attached Image:</strong>
                    <div style="margin-top: 0.5rem;">
                        <img src="{{ issue.image.url }}" alt="Issue Image" style="max-width: 300px; border-radius: 5px;">
                    </div>
                </div>
                {% endif %}
                
                <h3>Status Updates</h3>
                <div style="border-left: 3px solid #3498db; padding-left: 1rem;">
                    {% for update in updates %}
                    <div style="margin-bottom: 1.5rem; padding: 1rem; background: white; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: between; margin-bottom: 0.5rem;">
                            <strong>{{ update.updated_by.username }}</strong>
                            <small style="color: #666;">{{ update.created_at|date:"M d, Y H:i" }}</small>
                        </div>
                        <p style="margin: 0; color: #333;">{{ update.update_text }}</p>
                    </div>
                    {% empty %}
                    <div style="padding: 1rem; background: white; border-radius: 5px; text-align: center; color: #666;">
                        No updates yet. Your issue is being reviewed.
                    </div>
                    {% endfor %}
                </div>
                
                <div style="margin-top: 2rem; text-align: center;">
                    <a href="{% url 'track_issue' %}" class="btn btn-secondary">← Back to All Issues</a>
                </div>
            </div>
            
        {% else %}
            <!-- All Issues View -->
            <div class="card">
                <h2 style="text-align: center; margin-bottom: 2rem; color: #2c3e50;">Track Your Issues</h2>
                
                {% if messages %}
                <div class="messages">
                    {% for message in messages %}
                    <div class="alert alert-{{ message.tags }}">
                        {{ message }}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                
                <!-- Search Form -->
                <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 5px; margin-bottom: 2rem;">
                    <h4 style="margin-bottom: 1rem;">🔍 Search by Ticket ID</h4>
                    <form method="post" style="display: flex; gap: 1rem;">
                        {% csrf_token %}
                        <input type="text" name="ticket_id" placeholder="Enter Ticket ID (e.g., UAP12345678)" 
                               class="form-control" style="flex: 1;" required>
                        <button type="submit" class="btn">Search</button>
                    </form>
                </div>
                
                <!-- User's Issues List -->
                <h3>Your Recent Issues</h3>
                {% if user_issues %}
                    <div style="display: grid; gap: 1rem;">
                        {% for issue in user_issues %}
                        <div style="background: white; padding: 1.5rem; border-radius: 5px; border-left: 4px solid 
                                    {% if issue.status == 'resolved' %}#27ae60
                                    {% elif issue.status == 'in_progress' %}#f39c12
                                    {% else %}#3498db{% endif %}; 
                                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 1rem;">
                                <div style="flex: 1;">
                                    <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">
                                        {{ issue.get_category_display }}
                                    </h4>
                                    <p style="margin: 0; color: #666; font-size: 0.9rem;">
                                        <strong>Ticket ID:</strong> {{ issue.ticket_id }} | 
                                        <strong>Department:</strong> {{ issue.get_department_display }} |
                                        <strong>Location:</strong> {{ issue.location }}
                                    </p>
                                </div>
                                <div style="text-align: right;">
                                    <span class="status-badge status-{{ issue.status }}" 
                                          style="padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                                        {{ issue.status|title }}
                                    </span>
                                    <div style="margin-top: 0.5rem;">
                                        <a href="{% url 'track_issue_detail' issue.ticket_id %}" class="btn" style="padding: 0.3rem 0.8rem; font-size: 0.8rem;">
                                            View Details
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <p style="margin: 0; color: #333; font-size: 0.9rem;">
                                {{ issue.description|truncatewords:20 }}
                            </p>
                            <div style="margin-top: 1rem; font-size: 0.8rem; color: #666;">
                                Reported on {{ issue.created_at|date:"M d, Y" }}
                                {% if issue.anonymous %}(Reported Anonymously){% endif %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div style="text-align: center; padding: 3rem; color: #666;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">📝</div>
                        <h3>No Issues Reported Yet</h3>
                        <p>You haven't reported any issues yet. Click the button below to report your first issue!</p>
                        <a href="{% url 'report_issue' %}" class="btn" style="margin-top: 1rem;">Report New Issue</a>
                    </div>
                {% endif %}
            </div>
        {% endif %}
    </div>
</div>

<style>
    .status-badge {
        text-transform: capitalize;
    }
    
    .status-pending {
        background: #3498db;
        color: white;
    }
    
    .status-in_progress {
        background: #f39c12;
        color: white;
    }
    
    .status-resolved {
        background: #27ae60;
        color: white;
    }
    
    .status-closed {
        background: #7f8c8d;
        color: white;
    }
</style>
{% endblock %}'''

    with open('campus_fixer/templates/campus_fixer/track_issue.html', 'w', encoding='utf-8') as f:
        f.write(track_issue_html)
    print("✅ track_issue.html created")

    # 3. Update dashboard.html to show actual user data
    print("📈 Updating dashboard.html...")
    dashboard_html = '''{% extends 'campus_fixer/base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="content">
    <div class="container">
        <div class="card">
            <h2>Welcome, {{ user.username }}! 👋</h2>
            <p>This is your dashboard. From here you can manage all your maintenance requests.</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 2rem;">
                <a href="{% url 'report_issue' %}" class="btn" style="text-align: center; display: flex; flex-direction: column; align-items: center;">
                    <span style="font-size: 2rem; margin-bottom: 0.5rem;">📝</span>
                    Report New Issue
                </a>
                <a href="{% url 'track_issue' %}" class="btn btn-secondary" style="text-align: center; display: flex; flex-direction: column; align-items: center;">
                    <span style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</span>
                    Track Issues
                </a>
            </div>
        </div>
        
        <div class="card">
            <h3>Quick Stats</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1rem;">
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 5px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #3498db;">{{ total_issues }}</div>
                    <div>Total Issues</div>
                </div>
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 5px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #f39c12;">{{ pending_issues }}</div>
                    <div>Pending</div>
                </div>
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 5px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #27ae60;">{{ resolved_issues }}</div>
                    <div>Resolved</div>
                </div>
            </div>
        </div>

        {% if user_issues %}
        <div class="card">
            <h3>Recent Issues</h3>
            <div style="display: grid; gap: 1rem;">
                {% for issue in user_issues %}
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 5px; border-left: 4px solid 
                            {% if issue.status == 'resolved' %}#27ae60
                            {% elif issue.status == 'in_progress' %}#f39c12
                            {% else %}#3498db{% endif %};">
                    <div style="display: flex; justify-content: between; align-items: center;">
                        <div style="flex: 1;">
                            <strong>{{ issue.get_category_display }}</strong>
                            <div style="font-size: 0.9rem; color: #666;">
                                {{ issue.ticket_id }} • {{ issue.location }}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <span style="padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold;
                                    background: {% if issue.status == 'resolved' %}#27ae60
                                    {% elif issue.status == 'in_progress' %}#f39c12
                                    {% else %}#3498db{% endif %}; color: white;">
                                {{ issue.status|title }}
                            </span>
                            <div style="margin-top: 0.5rem;">
                                <a href="{% url 'track_issue_detail' issue.ticket_id %}" style="font-size: 0.8rem; color: #3498db;">
                                    View Details
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="{% url 'track_issue' %}" class="btn btn-secondary">View All Issues</a>
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}'''

    with open('campus_fixer/templates/campus_fixer/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    print("✅ dashboard.html updated")

    # 4. Create admin.py for admin panel
    print("⚙️ Creating admin.py...")
    admin_content = '''from django.contrib import admin
from .models import UserProfile, Issue, IssueUpdate, Feedback

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'department']
    list_filter = ['user_type', 'department']
    search_fields = ['user__username']

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'category', 'department', 'status', 'created_at']
    list_filter = ['status', 'category', 'department', 'created_at']
    search_fields = ['ticket_id', 'user__username', 'description', 'location']
    readonly_fields = ['ticket_id', 'created_at']

@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ['issue', 'updated_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['issue__ticket_id', 'update_text']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['issue', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['issue__ticket_id', 'comment']
'''

    with open('campus_fixer/admin.py', 'w', encoding='utf-8') as f:
        f.write(admin_content)
    print("✅ admin.py created")

def main():
    print("🚀 APPLYING FUNCTIONAL TEMPLATES FIX...")
    print("=" * 60)
    
    create_functional_templates()
    
    print("\n" + "=" * 60)
    print("🎉 FUNCTIONAL TEMPLATES CREATED SUCCESSFULLY!")
    print("\n🚀 Now test these features:")
    print("   1. Go to Dashboard - should show your stats")
    print("   2. Click 'Report New Issue' - should show working form")
    print("   3. Fill out the form and submit - should create an issue")
    print("   4. Click 'Track Issues' - should show your reported issues")
    print("   5. Click 'View Details' - should show issue details")
    print("\n✅ Report Issue and Track Issue should now work perfectly!")

if __name__ == "__main__":
    main()
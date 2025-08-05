from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard - only one definition needed
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Threat alerts - consistent naming (using underscores)
    path('threat_alerts/', views.threat_alerts, name='threat_alerts'),
    path('threat_alerts/<int:alert_id>/', views.alert_detail, name='alert_detail'),
    
    # Alert creation
    path('create_alert/', views.create_alert, name='create_alert'),
    
    # Resources
    path('resources/', views.resources_view, name='resources'),
    
    # Admin reports
    path('admin/reports/', views.admin_reports, name='admin_reports'),
]
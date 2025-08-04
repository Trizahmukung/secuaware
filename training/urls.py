from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('threat_alerts/', views.threat_alerts, name='threat_alerts'),
    path('threat_alerts/<int:alert_id>/', views.threat_alert_detail, name='threat_alert_detail'),
    path('create_alert/', views.create_alert, name='create_alert'),
]
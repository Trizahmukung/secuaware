from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from .models import ThreatAlert, UserAlert, UserProgress, TrainingModule
from django.db.models import Count, Avg, Max
from django.contrib.auth.models import User
from .forms import ThreatAlertForm

# 👇 Home view 
def home(request):
    return HttpResponse("Welcome to the Cybersecurity Awareness Platform!")

# 👇 Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        messages.error(request, "Please correct the errors below")
    else:
        form = UserCreationForm()
    return render(request, 'training/register.html', {'form': form})

# 👇 Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None: 
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'training/login.html', {'form': form})

@login_required
def dashboard(request):
    completed = UserProgress.objects.filter(user=request.user, completed=True).count()
    in_progress = UserProgress.objects.filter(user=request.user, completed=False).count()
    # recent_alerts = ThreatAlert.objects.filter(is_active=True).order_by('-created_at')[:3]
    recent_alerts = ThreatAlert.objects.filter(is_active=True).order_by('-date_posted')[:3]

    context = {
        'completed': completed,
        'in_progress': in_progress,
        'recent_alerts': recent_alerts,
    }
    return render(request, 'training/dashboard.html', context)

@login_required
def threat_alerts(request):
    alerts = ThreatAlert.objects.filter(is_active=True).order_by('-date_posted')
    # Mark unread alerts for the current user
    for alert in alerts:
        UserAlert.objects.get_or_create(user=request.user, alert=alert)
    return render(request, 'training/threat_alerts.html', {'alerts': alerts})

@login_required
def alert_detail(request, alert_id):
    alert = get_object_or_404(ThreatAlert, id=alert_id)
    user_alert = UserAlert.objects.get(user=request.user, alert=alert)
    if not user_alert.read:
        user_alert.read = True
        user_alert.save()
    return render(request, 'training/alert_detail.html', {'alert': alert})

@login_required
def create_alert(request):
    if not request.user.is_staff:
        return redirect('threat_alerts')
    if request.method == 'POST':
        form = ThreatAlertForm(request.POST)
        if form.is_valid():
            alert = form.save()
            return redirect('alert_detail', alert_id=alert.id)
    else:
        form = ThreatAlertForm()
    return render(request, 'training/create_alert.html', {'form': form})

def threat_alert_detail(request, alert_id):
    alert = get_object_or_404(ThreatAlert, id=alert_id)
    context = {
        'alert': alert
    }
    return render(request, 'training/threat_alert_detail.html', context)

#  Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

@staff_member_required
def admin_reports(request):
    # Module completion stats
    module_stats = TrainingModule.objects.annotate(
        completions=Count('userprogress'),
        avg_score=Avg('userprogress__quiz_score')
    ).order_by('-completions')
    
    # User activity
    active_users = User.objects.annotate(
        module_count=Count('userprogress'),
        last_active=Max('userprogress__last_accessed')
    ).order_by('-last_active')[:10]
    
    return render(request, 'training/admin_reports.html', {
        'module_stats': module_stats,
        'active_users': active_users,
    })


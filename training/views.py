from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Max, Sum
from django.utils import timezone
from datetime import timedelta
from .models import ThreatAlert, UserAlert, UserProgress, TrainingModule, UserBadge, EducationalResource
from .forms import ThreatAlertForm

def home(request):
    return render(request, 'training/home.html')

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
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    completed = UserProgress.objects.filter(user=request.user, completed=True).count()
    in_progress = UserProgress.objects.filter(user=request.user, completed=False).count()
    recent_alerts = ThreatAlert.objects.filter(is_active=True).order_by('-date_posted')[:3]
    
    # Get unread alerts count for the badge
    unread_alerts_count = UserAlert.objects.filter(
        user=request.user,
        read=False
    ).count()

    context = {
        'completed': completed,
        'in_progress': in_progress,
        'recent_alerts': recent_alerts,
        'unread_alerts_count': unread_alerts_count
    }
    return render(request, 'training/dashboard.html', context)

@login_required
def threat_alerts(request):
    alerts = ThreatAlert.objects.filter(is_active=True).order_by('-date_posted')
    # Create UserAlert records if they don't exist
    for alert in alerts:
        UserAlert.objects.get_or_create(user=request.user, alert=alert)
    return render(request, 'training/threat_alerts.html', {'alerts': alerts})

@login_required
def alert_detail(request, alert_id):
    alert = get_object_or_404(ThreatAlert, id=alert_id)
    user_alert, created = UserAlert.objects.get_or_create(
        user=request.user,
        alert=alert
    )
    if not user_alert.read:
        user_alert.read = True
        user_alert.save()
    return render(request, 'training/alert_detail.html', {'alert': alert})

@staff_member_required
def create_alert(request):
    if request.method == 'POST':
        form = ThreatAlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.author = request.user
            alert.save()
            return redirect('alert_detail', alert_id=alert.id)
    else:
        form = ThreatAlertForm()
    return render(request, 'training/create_alert.html', {'form': form})

@login_required
def resources_view(request):
    resources = EducationalResource.objects.all()
    return render(request, 'training/resources.html', {'resources': resources})

@staff_member_required
def admin_reports(request):
    module_stats = TrainingModule.objects.annotate(
        completions=Count('userprogress'),
        avg_score=Avg('userprogress__quiz_score')
    ).order_by('-completions')
    
    active_users = User.objects.annotate(
        module_count=Count('userprogress'),
        last_active=Max('userprogress__completion_date')
    ).order_by('-last_active')[:10]
    
    return render(request, 'training/admin_reports.html', {
        'module_stats': module_stats,
        'active_users': active_users,
    })

@login_required
def user_dashboard(request):
    completed = UserProgress.objects.filter(
        user=request.user,
        completed=True
    ).select_related('module')
    
    in_progress = UserProgress.objects.filter(
        user=request.user,
        completed=False
    ).select_related('module')
    
    total_time = sum([p.time_spent for p in completed if p.time_spent]) if completed else 0
    avg_time = total_time / len(completed) if completed else 0
    
    badges = UserBadge.objects.filter(user=request.user)
    
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    weekly_completed = completed.filter(
        completion_date__gte=week_ago
    ).count()
    
    context = {
        'completed': completed,
        'in_progress': in_progress,
        'total_time': round(total_time),
        'avg_time': round(avg_time, 1),
        'badges': badges,
        'weekly_completed': weekly_completed,
        'completion_percentage': calculate_completion(request.user),
    }
    return render(request, 'training/user_dashboard.html', context)

def calculate_completion(user):
    total_resources = EducationalResource.objects.count()
    if total_resources == 0:
        return 0
    completed_resources = UserProgress.objects.filter(
        user=user,
        completed=True
    ).count()
    return int((completed_resources / total_resources) * 100)
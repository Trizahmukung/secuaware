from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib import messages 
from django.contrib.auth.decorators import login_required  

# 👇 Home view (just to verify login worked)
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
    context = {
        'user': request.user,
        'active_menu': 'dashboard'
    }
    return render(request, 'training/dashboard/main.html', context)

#  Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

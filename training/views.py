from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse

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
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'training/register.html', {'form': form})

# 👇 Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'training/login.html', {'form': form})

# 👇 Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

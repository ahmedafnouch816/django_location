from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Vehicule
from django.core.files.storage import FileSystemStorage

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Create user manually
        if password1 == password2:
            try:
                user = User.objects.create_user(
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1
                )
                user.save()
                auth_login(request, user)
                messages.success(request, "Registration successful")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')


def logout_view(request):
    """Log out the user and redirect to the home page."""
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to home page or any other page


@login_required
def profile_view(request):
    """Render the user's profile page."""
    return render(request, 'profile.html', {'user': request.user})

@login_required
def home_view(request):
    return render(request, 'home.html')

def dashboard(request):
    # You can add context data here if needed
    return render(request, 'dashboard.html')

from .forms import VehiculeForm 

def add_vehicule(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form data:", form.cleaned_data)
            form.save()
            return redirect('some_view_name')
        else:
            print("Form errors:", form.errors)
            return render(request, 'add_vehicule.html', {'form': form, 'error_message': form.errors})
    else:
        form = VehiculeForm()
    return render(request, 'add_vehicule.html', {'form': form})

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User

from garbage_classification.settings import EMAIL_HOST_USER

from .forms import SignUpForm, ProfileForm
from .models import Profile, TokenTransaction

import random

def admin_dashboard(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        current_profile = Profile.objects.get(user=current_user)

        return render(request, 'dashboard.html', {'current_user':current_user, 'current_profile':current_profile})
    else:
        return render(request, 'login.html', {})

def admin_login(request):
    if request.user.is_authenticated:
        messages.success(request, "You have been logged in.")
        return redirect('garbage_admin_dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in.")
                return redirect('garbage_admin_dashboard')
            else:
                messages.success(request, "Invalid username and password. Please try again!.")
                return render(request, 'login.html', {})
        else:
            return render(request, 'login.html', {})



def admin_register(request):
    if request.user.is_authenticated:
        messages.success(request, "You have been logged in.")
        return redirect('garbage_admin_dashboard')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                # Authenticate and login
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                current_user = User.objects.get(username=user)
                current_profile = Profile()
                current_profile.otp = random.randint(1000000, 9999999)
                current_profile.user = current_user
                current_profile.save()
                token_transactions = TokenTransaction()
                token_transactions.amount = 1000
                token_transactions.user = current_user
                token_transactions.transaction_type = 'credit'
                token_transactions.save()
                current_profile.tokens += token_transactions.amount
                current_profile.save()
                messages.success(request, "You Have Successfully Registered! Welcome!")
                return redirect('garbage_admin_dashboard')
        else:
            form = SignUpForm()
            return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})



def profile_update(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        current_profile = Profile.objects.get(user=current_user)
        if request.method == 'GET':
            form = ProfileForm(instance=current_profile)
            return render(request, 'profile_update.html', {'form':form})
        elif request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                current_profile.phone = form.cleaned_data['phone']
                current_profile.address = form.cleaned_data['address']
                current_profile.city = form.cleaned_data['city']
                current_profile.state = form.cleaned_data['state']
                current_profile.zipcode = form.cleaned_data['zipcode']
                current_profile.save()
                messages.success(request, "You Have Successfully Updated Your Profile.")
                return redirect('garbage_admin_profile')
            else:
                return render(request, 'profile_update.html', {'form':form})
    else:
        return render(request, 'login.html', {})



def admin_logout(request):
    logout(request)
    messages.success(request, "You have logged out.")
    return redirect('garbage_admin_login')



def admin_forgot_password(request):
    if request.user.is_authenticated:
        messages.success(request, "You have been logged in.")
        return redirect('garbage_admin_dashboard')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                # TODO Send Email
                user = User.objects.get(email=email)
                profile = Profile.objects.get(user=user)
                send_mail(
                    "Reset your password : Garbage Classification Application",
                    f"Hey {user}, want to reset password. Click on the link http://127.0.0.1:8000/garbage_admin/reset_password?username={user}&otp={profile.otp}",
                    EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f"Reset password link has been sent to your {email}.")
                return render(request, 'forgot_password.html', {})
            else:
                messages.success(request, f"{email} does not exist.")
                return render(request, 'forgot_password.html', {})
        else:
            return render(request, 'forgot_password.html', {})



def admin_reset_password(request):
    if request.user.is_authenticated:
        messages.success(request, "You have been logged in.")
        return redirect('garbage_admin_dashboard')
    else:
        if request.method == 'GET':
            username = request.GET['username']
            otp = request.GET['otp']
            return render(request, 'reset_password.html', {'username':username, 'otp':otp})
        elif request.method == 'POST':
            username = request.POST['username']
            otp = request.POST['otp']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    db_user = User.objects.get(username=username)
                    db_profile = Profile.objects.get(user=db_user)
                    if db_profile.otp == otp:
                        db_user.set_password(password1)
                        db_user.save()
                        messages.success(request, f"Password has been reset. Try to login with new password")
                        return redirect('garbage_admin_login')
                    else:
                        messages.success(request, f"Password do not match. Try again")
                        return render(request, 'reset_password.html', {'username':username, 'otp':otp})
            else:
                messages.success(request, f"Password do not match. Try again")
                return render(request, 'reset_password.html', {'username':username, 'otp':otp})
        else:
            return redirect('garbage_admin_login')
        
def profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        current_profile = Profile.objects.get(user=current_user)
        token_transactions = TokenTransaction.objects.get(user=current_user)
        return render(request, 'profile.html', {'current_user':current_user, 'current_profile':current_profile, 'token_transactions':token_transactions})
    else:
        return render(request, 'login.html', {})

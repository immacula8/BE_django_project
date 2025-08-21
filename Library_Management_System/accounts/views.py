from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('subscription_plan', 'country', 'profile_photo')}),
    )

# Registration view
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  # redirect to homepage after signup
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# Login view
def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # redirect after login
    else:
        form = CustomAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect("login")

def home_view(request):
    return render(request, "accounts/home.html")

@login_required
def subscribe_view(request):
    user = request.user
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            user.subscription_plan = form.cleaned_data['plan']
            user.save()
            return render(request, "accounts/subscribe_success.html", {"plan": user.subscription_plan})
    else:
        form = SubscriptionForm(initial={"plan": user.subscription_plan})
    return render(request, "accounts/subscribe.html", {"form": form})
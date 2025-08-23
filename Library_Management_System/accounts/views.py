from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.admin import UserAdmin
from .forms import SubscriptionForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Subscription
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

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

@login_required
def home(request):
    return render(request, "accounts/home.html")

@login_required
def subscribe_view(request):
    try:
        subscription = request.user.subscription
    except Subscription.DoesNotExist:
        subscription = Subscription(user=request.user)

    if request.method == "POST":
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            plan_type = form.cleaned_data["plan_type"]
            auto_renew = form.cleaned_data["auto_renew"]

            # start subscription for 30 days
            subscription.start_subscription(plan_type, duration_days=30, auto_renew=auto_renew)

            return redirect("subscription_detail")
    else:
        form = SubscriptionForm(instance=subscription)

    return render(request, "accounts/subscribe.html", {"form": form})

@login_required
def dashboard_view(request):
    # Instead of showing borrowed books (Borrow model is removed),
    # we just show user info and their subscription plan
    return render(request, "accounts/dashboard.html", {"user": request.user})

@login_required
def subscription_detail(request):
    subscription = getattr(request.user, "subscription", None)
    plan = subscription.plan_type if subscription else "free"
    return render(request, "accounts/subscription_detail.html", {"subscription": subscription})


@login_required
def upgrade(request, plan):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        subscription, created = Subscription.objects.get_or_create(user=request.user)

        if payment_method:
            # Update subscription record (not user anymore)
            subscription.plan_type = plan
            subscription.save()

            messages.success(request, f"Successfully upgraded to {plan}!")
            return redirect("book_list")
        else:
            messages.error(request, "Payment failed. Try again.")

    return render(request, "accounts/upgrade.html", {"plan": plan})
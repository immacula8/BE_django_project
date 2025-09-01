from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.admin import UserAdmin
from .forms import SubscriptionForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Subscription
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from books.models import Book 
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Comment
from .forms import CommentForm
from django.shortcuts import render
from .forms import PaymentForm
from django.contrib.auth import login

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
    # show a first-cut selection of books available
    available_books = Book.objects.all().select_related("author")[:30]
    return render(request, "accounts/dashboard.html", {"available_books": available_books})

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
            subscription.plan_type = plan  # e.g. 'premium' or 'unlimited'
            subscription.save()
            # keep the quick-access field on the user in sync (legacy)
            request.user.subscription_plan = plan.upper()
            request.user.save(update_fields=["subscription_plan"])
            messages.success(request, f"Successfully upgraded to {plan.title()}!")
            return redirect("book_list")
        else:
            messages.error(request, "Payment failed. Try again.")
    return render(request, "accounts/upgrade.html", {"plan": plan})

@login_required
def comments_list(request):
    comments = request.user.comments.all().order_by("-created_at")
    form = CommentForm()
    return render(request, "accounts/comments.html", {"comments": comments, "form": form})

@login_required
def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment was posted. Thank you!")
            return redirect("comments")
    return redirect("comments")

@staff_member_required
def reply_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        reply_text = request.POST.get("reply")
        if reply_text:
            comment.reply = reply_text
            comment.replied_by = request.user
            comment.replied_at = timezone.now()
            comment.save()
            messages.success(request, "Reply sent to user.")
            return redirect("admin:accounts_comment_changelist")  # send admin back to comment list in admin
    # for GET, you might render a simple reply form (optional)
    return render(request, "accounts/reply_comment.html", {"comment": comment})

def subscribe(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process the payment here (e.g., call Stripe/Paystack API)
            return render(request, "accounts/success.html")
    else:
        form = PaymentForm()

    return render(request, "accounts/subscribe.html", {"form": form})

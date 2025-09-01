from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    subscription_plan = models.CharField(
        max_length=20,
        choices=[('FREE', 'Free'), ('PREMIUM', 'Premium'), ('UNLIMITED', 'Unlimited')],
        default='FREE'
    )
    country = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    @property
    def is_premium(self):
        # prefer the Subscription object if present; fall back to the user field
        sub = getattr(self, "subscription", None)
        if sub:
            return sub.plan_type == "premium"
        return (self.subscription_plan or "").lower() == "premium"

    @property
    def is_unlimited(self):
        sub = getattr(self, "subscription", None)
        if sub:
            return sub.plan_type == "unlimited"
        return (self.subscription_plan or "").lower() == "unlimited"

    @property
    def current_plan(self):
        sub = getattr(self, "subscription", None)
        if sub:
            return sub.plan_type
        return (self.subscription_plan or "free").lower()


    def __str__(self):
        return self.username


class Subscription(models.Model):
    PLAN_CHOICES = [
        ("free", "Free"),
        ("premium", "Premium"),
        ("unlimited", "Unlimited"),
    ]

    PLAN_PRICES = {
        "free": 0,
        "premium": 10,       # $10 per month
        "unlimited": 100,    # $100 per month
    }

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default="free")
    books_read_this_month = models.PositiveIntegerField(default=0)
    subscription_expiry = models.DateField(null=True, blank=True)
    last_count_reset = models.DateField(null=True, blank=True)

    # NEW FIELD: auto debit or manual payment
    auto_renew = models.BooleanField(default=False, help_text="Automatically renew subscription?")

    def is_active(self):
        if self.subscription_expiry is None:
            return False
        return timezone.now().date() <= self.subscription_expiry

    @property
    def max_books_per_month(self):
        if self.plan_type == "premium":
            return 5
        if self.plan_type == "free":
            return 0
        return None  # unlimited

    @property
    def monthly_fee(self):
        return self.PLAN_PRICES.get(self.plan_type, 0)

    def reset_month_if_needed(self):
        today = timezone.now().date()
        month_key_today = today.strftime("%Y-%m")
        if not self.last_count_reset or self.last_count_reset.strftime("%Y-%m") != month_key_today:
            self.books_read_this_month = 0
            self.last_count_reset = today.replace(day=1)
            self.save(update_fields=["books_read_this_month", "last_count_reset"])

    def start_subscription(self, plan_type, duration_days=30, auto_renew=False):
        self.plan_type = plan_type
        self.subscription_expiry = timezone.now().date() + timedelta(days=duration_days)
        self.books_read_this_month = 0
        self.last_count_reset = timezone.now().date().replace(day=1)
        self.auto_renew = auto_renew
        self.save()

    def __str__(self):
        renew_status = "Auto" if self.auto_renew else "Manual"
        return f"{self.user.username} - {self.plan_type} ({renew_status})"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    reply = models.TextField(blank=True, null=True)
    replied_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="comment_replies", on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.user.username} at {self.created_at}"
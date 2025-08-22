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

    def __str__(self):
        return self.username
    
class Subscription(models.Model):
    PLAN_CHOICES = [
        ("free", "Free"),
        ("premium", "Premium"),
        ("unlimited", "Unlimited"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default="free")
    books_read_this_month = models.PositiveIntegerField(default=0)
    subscription_expiry = models.DateField(null=True, blank=True)

    def is_active(self):
        """Check if subscription is valid (not expired)."""
        if self.subscription_expiry is None:
            return False
        return timezone.now().date() <= self.subscription_expiry

    def start_subscription(self, plan_type, duration_days=30):
        """Helper to set up or renew a subscription."""
        self.plan_type = plan_type
        self.subscription_expiry = timezone.now().date() + timedelta(days=duration_days)
        self.books_read_this_month = 0  # reset counter
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.plan_type}"

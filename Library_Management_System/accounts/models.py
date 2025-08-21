from django.contrib.auth.models import AbstractUser
from django.db import models


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

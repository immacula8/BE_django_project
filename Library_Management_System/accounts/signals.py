from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from books.models import LibraryMember
from django.conf import settings
from .models import Subscription

@receiver(post_save, sender=CustomUser)
def create_library_member(sender, instance, created, **kwargs):
    if created:
        LibraryMember.objects.create(user=instance)

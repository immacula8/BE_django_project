from django.db import models
from accounts.models import CustomUser
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class LibraryMember(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    borrowed_books = models.ManyToManyField('Book', blank=True)
    subscription_active = models.BooleanField(default=False)
    subscription_expiry = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)  # Use your existing Book model
    borrowed_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank=True, null=True)
    returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.borrowed_at + timedelta(days=14)
        super().save(*args, **kwargs)

    def is_overdue(self):
        return timezone.now() > self.due_date and not self.returned

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
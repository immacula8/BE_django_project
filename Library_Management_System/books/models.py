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


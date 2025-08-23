 # books/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime

def current_month():
    return datetime.date.today().month 

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
    copies_available = models.PositiveIntegerField()  # can keep if you still want inventory
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)

    # Content
    preview_text = models.TextField(blank=True)   # visible to Free
    full_text = models.TextField(blank=True)      # full content for reading online
    file = models.FileField(upload_to="books/files/", blank=True, null=True)  # for Unlimited downloads

    def __str__(self):
        return f"{self.title} by {self.author}"

class ReadingList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reading_list")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user} saved {self.book}"

class BookAccess(models.Model):
    """
    Track per-user, per-book, per-month access so we can count unique 'full reads'
    for premiums and enforce the monthly cap.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    month_key = models.IntegerField(default=current_month) 
    first_opened = models.DateTimeField(auto_now=True)
    counted = models.BooleanField(default=False)  # set True when it increments the monthly counter

    class Meta:
        unique_together = ("user", "book", "month_key")

    def __str__(self):
        return f"{self.user} opened {self.book} in {self.month_key}"

class AuthorSubmission(models.Model):
    PAYMENT_CHOICES = [
        ("unlimited_fee", "Yearly Unlimited Fee"),
        ("revshare_20", "20% Revenue Share"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    author_name = models.CharField(max_length=120)
    author_email = models.EmailField()
    author_bio = models.TextField(blank=True)

    book_title = models.CharField(max_length=200)
    description = models.TextField()
    manuscript = models.FileField(upload_to="submissions/")
    payment_choice = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book_title} by {self.author_name} ({self.payment_choice})"

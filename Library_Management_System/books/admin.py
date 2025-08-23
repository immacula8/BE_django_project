# books/admin.py
from django.contrib import admin
from .models import Book, Author, ReadingList, BookAccess, AuthorSubmission

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "author__name", "isbn")

admin.site.register(Author)
admin.site.register(ReadingList)
admin.site.register(BookAccess)

@admin.register(AuthorSubmission)
class AuthorSubmissionAdmin(admin.ModelAdmin):
    list_display = ("book_title", "author_name", "payment_choice", "status", "submitted_at")
    list_filter = ("payment_choice", "status")
    search_fields = ("book_title", "author_name", "author_email")

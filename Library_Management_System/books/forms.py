# books/forms.py
from django import forms
from .models import AuthorSubmission
from .models import Book

class AuthorSubmissionForm(forms.ModelForm):
    class Meta:
        model = AuthorSubmission
        fields = ["author_name", "author_email", "author_bio",
                  "book_title", "description", "manuscript", "payment_choice"]

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "isbn", "copies_available", "author"]
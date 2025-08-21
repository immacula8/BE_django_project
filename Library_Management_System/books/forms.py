from django import forms
from .models import Borrow, Book

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['book']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only books that have available copies
        self.fields['book'].queryset = Book.objects.filter(copies_available__gt=0)

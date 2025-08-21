from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BorrowForm
from .models import Borrow

@login_required
def borrow_book_view(request):
    form = BorrowForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        borrow = form.save(commit=False)
        borrow.user = request.user

        # Reduce available copies of the book
        borrow.book.copies_available -= 1
        borrow.book.save()

        borrow.save()
        return redirect("borrow_history")  # We'll create this view next

    return render(request, "books/borrow.html", {"form": form})

@login_required
def borrow_history_view(request):
    borrows = Borrow.objects.filter(user=request.user)
    return render(request, "books/borrow_history.html", {"borrows": borrows})


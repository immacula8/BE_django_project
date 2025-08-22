from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book
from django.contrib import messages

@login_required
def read_book_view(request, book_id):
    book = Book.objects.get(id=book_id)
    
    if request.user.subscription_plan not in ["premium", "unlimited"]:
        # Show a friendly message
        messages.warning(
            request,
            "You cannot read online unless you have a Premium or Unlimited plan. Upgrade below."
        )
        return redirect("subscribe")  # Redirect to the subscription page
    
    # If user is premium/unlimited, show the book
    return render(request, "books/read_online.html", {"book": book})

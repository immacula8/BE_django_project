from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import Subscription
from .models import Book, ReadingList, BookAccess, AuthorSubmission
from .forms import AuthorSubmissionForm  
from .forms import BookForm
from rest_framework import generics
from .serializers import BookSerializer
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django.db.models import Avg
from .models import Review
from django.contrib.admin.views.decorators import staff_member_required

def _get_subscription(user) -> Subscription:
    sub, _ = Subscription.objects.get_or_create(user=user, defaults={"plan_type": "free"})
    return sub

def book_list(request):
    books = Book.objects.all().select_related("author")
    return render(request, "books/book_list.html", {"books": books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    plan = None
    if request.user.is_authenticated:
        plan = _get_subscription(request.user).plan_type

    # handle review posting
    if request.method == "POST" and request.user.is_authenticated:
        rating = int(request.POST.get("rating", 0))
        comment = request.POST.get("comment", "").strip()
        if 1 <= rating <= 5:
            Review.objects.create(user=request.user, book=book, rating=rating, comment=comment)
            messages.success(request, "Thank you for your review.")
            return redirect("book_detail", pk=pk)
        else:
            messages.error(request, "Please submit a rating between 1 and 5.")

    avg_rating = book.reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    return render(request, "books/book_detail.html", {"book": book, "plan_type": plan, "avg_rating": avg_rating})

@login_required
def read_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    sub = _get_subscription(request.user)

    if not sub.is_active() and sub.plan_type != "free":
        messages.warning(request, "Your subscription has expired. Please renew to continue reading.")
        return redirect("subscribe")

    # Free users: preview only
    if sub.plan_type == "free":
        messages.info(request, "Upgrade to Premium or Unlimited to read full books.")
        return redirect("subscribe")

    # Premium: enforce monthly cap (5 books)
    sub.reset_month_if_needed()
    if sub.plan_type == "premium":
        month_key = timezone.now().strftime("%Y-%m")
        access, created = BookAccess.objects.get_or_create(
            user=request.user, book=book, month_key=month_key
        )
        if created and sub.books_read_this_month >= 5:
            messages.warning(request, "You have reached your 5-book monthly limit. Upgrade to Unlimited for unlimited reading.")
            return redirect("subscribe")

        # count once per unique book per month
        if not access.counted:
            sub.books_read_this_month += 1
            sub.save(update_fields=["books_read_this_month"])
            access.counted = True
            access.save(update_fields=["counted"])

    # Unlimited: no gating
    return render(request, "books/read_full.html", {"book": book})

@login_required
def download_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    sub = _get_subscription(request.user)

    if sub.plan_type != "unlimited":
        messages.warning(request, "Downloads are for Unlimited members only.")
        return redirect("subscribe")

    if not book.file:
        raise Http404("No file available for this book.")
    return FileResponse(book.file.open("rb"), as_attachment=True, filename=f"{book.title}.pdf")

@login_required
def add_to_reading_list(request, pk):
    book = get_object_or_404(Book, pk=pk)
    ReadingList.objects.get_or_create(user=request.user, book=book)
    messages.success(request, f"“{book.title}” added to your reading list.")
    return redirect("my_reading_list")

@login_required
def my_reading_list(request):
    entries = ReadingList.objects.filter(user=request.user).select_related("book", "book__author")
    return render(request, "books/my_reading_list.html", {"entries": entries})

def submit_book(request):
    if request.method == "POST":
        form = AuthorSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your submission was received. We’ll review and get back to you!")
            return redirect("book_list")
    else:
        form = AuthorSubmissionForm()
    return render(request, "books/submit_book.html", {"form": form})

@staff_member_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "books/add_book.html", {"form": form})


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# ✅ Retrieve + Update + Delete Author
class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
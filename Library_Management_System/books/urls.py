from django.urls import path
from . import views
from .views import (
    book_list, book_detail, read_book, download_book, add_to_reading_list,
    my_reading_list, submit_book, add_book
)
from .api_views import BookListAPIView, BookDetailAPIView, AuthorListCreateAPIView, AuthorDetailAPIView

urlpatterns = [
    # Normal views
    path("", views.book_list, name="book_list"),
    path("<int:pk>/", views.book_detail, name="book_detail"),
    path("<int:pk>/read/", views.read_book, name="read_book"),
    path("<int:pk>/download/", views.download_book, name="download_book"),
    path("<int:pk>/save/", views.add_to_reading_list, name="add_to_reading_list"),
    path("my-list/", views.my_reading_list, name="my_reading_list"),
    path("submit/", views.submit_book, name="submit_book"),
    path("add/", views.add_book, name="add_book"),

    # API views (🚨 no extra "api/" here)
    path("", BookListAPIView.as_view(), name="api-book-list"),
    path("<int:pk>/", BookDetailAPIView.as_view(), name="api-book-detail"),
    path("authors/", AuthorListCreateAPIView.as_view(), name="api-authors"),
    path("authors/<int:pk>/", AuthorDetailAPIView.as_view(), name="api-author-detail"),
]

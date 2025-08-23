# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),                       # /books/
    path("<int:pk>/", views.book_detail, name="book_detail"),          # /books/12/
    path("<int:pk>/read/", views.read_book, name="read_book"),         # gated full read
    path("<int:pk>/download/", views.download_book, name="download_book"),  # unlimited only
    path("<int:pk>/save/", views.add_to_reading_list, name="add_to_reading_list"),
    path("my-list/", views.my_reading_list, name="my_reading_list"),
    path("submit/", views.submit_book, name="submit_book"),
    path("add/", views.add_book, name="add_book"),            # author submission
]

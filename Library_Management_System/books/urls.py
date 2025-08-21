from django.urls import path, include
from .views import borrow_book_view, borrow_history_view

urlpatterns = [
    path('borrow/', borrow_book_view, name='borrow_book'),
    path('history/', borrow_history_view, name='borrow_history'),
]
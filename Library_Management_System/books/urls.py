from django.urls import path
from .views import read_book_view

urlpatterns = [
    path('read/<int:book_id>/', read_book_view, name='read_book'),

]
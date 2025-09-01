from django.urls import path
from .api_views import (
    BookListAPIView, BookDetailAPIView,
    AuthorListCreateAPIView, AuthorDetailAPIView,
    ReserveBookAPIView, CommentAPIView
)

urlpatterns = [
    path("", BookListAPIView.as_view(), name="api-book-list"),
    path("<int:pk>/", BookDetailAPIView.as_view(), name="api-book-detail"),
    path("authors/", AuthorListCreateAPIView.as_view(), name="api-authors"),
    path("authors/<int:pk>/", AuthorDetailAPIView.as_view(), name="api-author-detail"),

    # 🚨 Add these
    path("reserve/", ReserveBookAPIView.as_view(), name="api-reserve"),
    path("comment/", CommentAPIView.as_view(), name="api-comment"),
]

from django.urls import path

from app.api.v1 import views

urlpatterns = [
    path("books/", views.BooksListAPIView.as_view(), name="book-list"),
]
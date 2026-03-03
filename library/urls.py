from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),
    # Books
    path("books/", views.book_list, name="book_list"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/create/", views.book_create, name="book_create"),
    path("books/<int:pk>/update/", views.book_update, name="book_update"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    # Authors
    path("authors/", views.author_list, name="author_list"),
    path("authors/<int:pk>/", views.author_detail, name="author_detail"),
    # Borrowings
    path("my-borrowings/", views.my_borrowings, name="my_borrowings"),
    path("books/<int:pk>/borrow/", views.borrow_book, name="borrow_book"),
    path("borrowings/<int:pk>/return/", views.return_book, name="return_book"),
    # Authentication
    path("register/", views.register, name="register"),
]

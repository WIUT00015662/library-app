from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Book, Author, Category, Borrowing
from .forms import BookForm


def home(request):
    """Home page view with featured books and statistics"""
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_categories = Category.objects.count()
    recent_books = Book.objects.order_by("-created_at")[:6]

    context = {
        "total_books": total_books,
        "total_authors": total_authors,
        "total_categories": total_categories,
        "recent_books": recent_books,
    }
    return render(request, "library/home.html", context)


def book_list(request):
    """List all books with optional filtering"""
    books = Book.objects.all()
    categories = Category.objects.all()

    # Filter by category
    category_id = request.GET.get("category")
    if category_id:
        books = books.filter(category_id=category_id)

    # Search by title
    search = request.GET.get("search")
    if search:
        books = books.filter(title__icontains=search)

    context = {
        "books": books,
        "categories": categories,
        "selected_category": category_id,
        "search": search,
    }
    return render(request, "library/book_list.html", context)


def book_detail(request, pk):
    """Book detail view"""
    book = get_object_or_404(Book, pk=pk)
    context = {"book": book}
    return render(request, "library/book_detail.html", context)


def author_list(request):
    """List all authors"""
    authors = Author.objects.all()
    context = {"authors": authors}
    return render(request, "library/author_list.html", context)


def author_detail(request, pk):
    """Author detail view with their books"""
    author = get_object_or_404(Author, pk=pk)
    books = author.books.all()
    context = {"author": author, "books": books}
    return render(request, "library/author_detail.html", context)


@login_required
def my_borrowings(request):
    """View user's borrowing history"""
    borrowings = Borrowing.objects.filter(user=request.user)
    context = {"borrowings": borrowings}
    return render(request, "library/my_borrowings.html", context)


@login_required
def borrow_book(request, pk):
    """Borrow a book"""
    book = get_object_or_404(Book, pk=pk)

    if not book.is_available:
        messages.error(request, "This book is not available for borrowing.")
        return redirect("book_detail", pk=pk)

    # Check if user already has this book
    existing = Borrowing.objects.filter(
        user=request.user, book=book, status="borrowed"
    ).exists()

    if existing:
        messages.warning(request, "You have already borrowed this book.")
        return redirect("book_detail", pk=pk)

    # Create borrowing record
    due_date = timezone.now().date() + timedelta(days=14)
    Borrowing.objects.create(user=request.user, book=book, due_date=due_date)

    # Update book availability
    book.available_copies -= 1
    book.save()

    messages.success(
        request, f'You have successfully borrowed "{book.title}". Due date: {due_date}'
    )
    return redirect("my_borrowings")


@login_required
def return_book(request, pk):
    """Return a borrowed book"""
    borrowing = get_object_or_404(
        Borrowing, pk=pk, user=request.user, status="borrowed"
    )

    borrowing.status = "returned"
    borrowing.returned_date = timezone.now().date()
    borrowing.save()

    # Update book availability
    borrowing.book.available_copies += 1
    borrowing.book.save()

    messages.success(
        request, f'You have successfully returned "{borrowing.book.title}".'
    )
    return redirect("my_borrowings")


# CRUD Operations for Books (Admin functionality)
@login_required
def book_create(request):
    """Create a new book"""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to add books.")
        return redirect("book_list")

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been created.')
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm()

    context = {"form": form, "action": "Create"}
    return render(request, "library/book_form.html", context)


@login_required
def book_update(request, pk):
    """Update an existing book"""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to edit books.")
        return redirect("book_list")

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been updated.')
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)

    context = {"form": form, "action": "Update", "book": book}
    return render(request, "library/book_form.html", context)


@login_required
def book_delete(request, pk):
    """Delete a book"""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete books.")
        return redirect("book_list")

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" has been deleted.')
        return redirect("book_list")

    context = {"book": book}
    return render(request, "library/book_confirm_delete.html", context)


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account created successfully! You can now log in."
            )
            return redirect("login")
    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)

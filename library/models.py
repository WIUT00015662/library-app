from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Author model - stores information about book authors"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    """Category model - for organizing books by genre/type"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model - main entity for library books
    Many-to-One: Book -> Category
    Many-to-Many: Book <-> Author
    """

    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    pages = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)

    # Many-to-One relationship with Category
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )

    # Many-to-Many relationship with Author
    authors = models.ManyToManyField(Author, related_name="books")

    available_copies = models.PositiveIntegerField(default=1)
    total_copies = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.available_copies > 0


class Borrowing(models.Model):
    """
    Borrowing model - tracks book loans
    Many-to-One: Borrowing -> Book
    Many-to-One: Borrowing -> User
    """

    STATUS_CHOICES = [
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
    ]

    # Many-to-One relationship with User
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")

    # Many-to-One relationship with Book
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")

    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="borrowed")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-borrowed_date"]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

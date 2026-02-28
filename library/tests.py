from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Author, Category, Book, Borrowing


class AuthorModelTest(TestCase):
    """Test Author model"""
    
    def setUp(self):
        self.author = Author.objects.create(
            first_name="John",
            last_name="Doe",
            bio="A famous author"
        )
    
    def test_author_creation(self):
        """Test that author is created correctly"""
        self.assertEqual(self.author.first_name, "John")
        self.assertEqual(self.author.last_name, "Doe")
        self.assertEqual(str(self.author), "John Doe")
    
    def test_author_full_name(self):
        """Test the full_name property"""
        self.assertEqual(self.author.full_name, "John Doe")


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Fiction",
            description="Fictional books"
        )
    
    def test_category_creation(self):
        """Test that category is created correctly"""
        self.assertEqual(self.category.name, "Fiction")
        self.assertEqual(str(self.category), "Fiction")


class BookModelTest(TestCase):
    """Test Book model"""
    
    def setUp(self):
        self.author = Author.objects.create(first_name="Jane", last_name="Smith")
        self.category = Category.objects.create(name="Science Fiction")
        self.book = Book.objects.create(
            title="Test Book",
            isbn="1234567890123",
            category=self.category,
            available_copies=5,
            total_copies=10
        )
        self.book.authors.add(self.author)
    
    def test_book_creation(self):
        """Test that book is created correctly"""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.isbn, "1234567890123")
        self.assertEqual(str(self.book), "Test Book")
    
    def test_book_availability(self):
        """Test is_available property"""
        self.assertTrue(self.book.is_available)
        self.book.available_copies = 0
        self.book.save()
        self.assertFalse(self.book.is_available)
    
    def test_book_relationships(self):
        """Test book relationships with author and category"""
        self.assertEqual(self.book.category, self.category)
        self.assertIn(self.author, self.book.authors.all())


class BorrowingModelTest(TestCase):
    """Test Borrowing model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.book = Book.objects.create(
            title="Borrowable Book",
            isbn="9876543210123",
            available_copies=3,
            total_copies=5
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            due_date=date.today() + timedelta(days=14)
        )
    
    def test_borrowing_creation(self):
        """Test that borrowing is created correctly"""
        self.assertEqual(self.borrowing.user, self.user)
        self.assertEqual(self.borrowing.book, self.book)
        self.assertEqual(self.borrowing.status, "borrowed")


class ViewsTest(TestCase):
    """Test views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.category = Category.objects.create(name="Mystery")
        self.author = Author.objects.create(first_name="Test", last_name="Author")
        self.book = Book.objects.create(
            title="Mystery Book",
            isbn="1111111111111",
            category=self.category,
            available_copies=2,
            total_copies=3
        )
        self.book.authors.add(self.author)
    
    def test_home_view(self):
        """Test home page loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/home.html')
    
    def test_book_list_view(self):
        """Test book list page loads correctly"""
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mystery Book")
    
    def test_book_detail_view(self):
        """Test book detail page loads correctly"""
        response = self.client.get(reverse('book_detail', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mystery Book")
    
    def test_author_list_view(self):
        """Test author list page loads correctly"""
        response = self.client.get(reverse('author_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Author")
    
    def test_my_borrowings_requires_login(self):
        """Test that my_borrowings requires authentication"""
        response = self.client.get(reverse('my_borrowings'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
    
    def test_borrow_book_authenticated(self):
        """Test borrowing a book when authenticated"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('borrow_book', args=[self.book.pk]))
        self.assertEqual(response.status_code, 302)  # Redirects after borrowing
        
        # Check that book was borrowed
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)
        
        # Check borrowing record exists
        borrowing = Borrowing.objects.filter(user=self.user, book=self.book).first()
        self.assertIsNotNone(borrowing)


class AuthenticationTest(TestCase):
    """Test authentication views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="authuser",
            password="authpass123"
        )
    
    def test_login_page_loads(self):
        """Test login page loads correctly"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_register_page_loads(self):
        """Test register page loads correctly"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_login(self):
        """Test user can login"""
        response = self.client.post(reverse('login'), {
            'username': 'authuser',
            'password': 'authpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after login


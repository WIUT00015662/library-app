from django.contrib import admin
from .models import Author, Category, Book, Borrowing


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'created_at')
    search_fields = ('first_name', 'last_name')
    list_filter = ('created_at',)
    ordering = ('last_name', 'first_name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'category', 'available_copies', 'total_copies', 'is_available')
    search_fields = ('title', 'isbn', 'authors__first_name', 'authors__last_name')
    list_filter = ('category', 'created_at')
    filter_horizontal = ('authors',)
    ordering = ('title',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'isbn', 'description', 'cover_image')
        }),
        ('Details', {
            'fields': ('authors', 'category', 'published_date', 'pages')
        }),
        ('Availability', {
            'fields': ('available_copies', 'total_copies')
        }),
    )


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'due_date', 'status', 'returned_date')
    search_fields = ('user__username', 'book__title')
    list_filter = ('status', 'borrowed_date', 'due_date')
    ordering = ('-borrowed_date',)
    
    fieldsets = (
        ('Borrowing Details', {
            'fields': ('user', 'book', 'status')
        }),
        ('Dates', {
            'fields': ('due_date', 'returned_date')
        }),
    )

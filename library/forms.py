from django import forms
from .models import Book, Author, Category


class BookForm(forms.ModelForm):
    """Form for creating and updating books"""

    class Meta:
        model = Book
        fields = [
            "title",
            "isbn",
            "description",
            "published_date",
            "pages",
            "cover_image",
            "category",
            "authors",
            "available_copies",
            "total_copies",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "published_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "pages": forms.NumberInput(attrs={"class": "form-control"}),
            "cover_image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "authors": forms.SelectMultiple(attrs={"class": "form-control"}),
            "available_copies": forms.NumberInput(attrs={"class": "form-control"}),
            "total_copies": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get("isbn")
        if isbn:
            # Remove any hyphens or spaces
            isbn = isbn.replace("-", "").replace(" ", "")
            if len(isbn) not in [10, 13]:
                raise forms.ValidationError("ISBN must be 10 or 13 characters long.")
        return isbn

    def clean(self):
        cleaned_data = super().clean()
        available = cleaned_data.get("available_copies")
        total = cleaned_data.get("total_copies")

        if available and total and available > total:
            raise forms.ValidationError("Available copies cannot exceed total copies.")
        return cleaned_data

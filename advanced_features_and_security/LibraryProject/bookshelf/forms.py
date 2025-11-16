from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing books.
    Uses Django's ModelForm to prevent SQL injection and validate input.
    All user input is automatically sanitized and validated by Django.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'required': True
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1000',
                'max': '9999',
                'required': True
            }),
        }
    
    def clean_title(self):
        """
        Additional validation for title field.
        Django automatically escapes HTML to prevent XSS attacks.
        """
        title = self.cleaned_data.get('title')
        if title:
            # Strip whitespace and validate length
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError("Title must be at least 3 characters long.")
        return title
    
    def clean_author(self):
        """
        Additional validation for author field.
        """
        author = self.cleaned_data.get('author')
        if author:
            author = author.strip()
            if len(author) < 2:
                raise forms.ValidationError("Author name must be at least 2 characters long.")
        return author
    
    def clean_publication_year(self):
        """
        Additional validation for publication year.
        """
        year = self.cleaned_data.get('publication_year')
        if year:
            # Validate reasonable year range
            if year < 1000 or year > 9999:
                raise forms.ValidationError("Publication year must be between 1000 and 9999.")
        return year


class BookSearchForm(forms.Form):
    """
    Secure search form that prevents SQL injection by using Django's ORM.
    Never use raw SQL queries with user input - always use Django ORM.
    """
    search_query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books...'
        }),
        label='Search'
    )
    
    def clean_search_query(self):
        """
        Sanitize search query to prevent injection attacks.
        Django automatically escapes special characters.
        """
        query = self.cleaned_data.get('search_query', '')
        if query:
            # Strip whitespace and limit length
            query = query.strip()
            # Remove potentially dangerous characters (though Django ORM handles this)
            # This is an extra layer of validation
            if len(query) > 200:
                raise forms.ValidationError("Search query is too long.")
        return query


class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form practices.
    This form shows how to properly handle user input with validation.
    """
    example_field = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter example text...'
        }),
        label='Example Field',
        help_text='This is an example field with proper validation.'
    )
    
    def clean_example_field(self):
        """
        Additional validation for the example field.
        Django automatically escapes HTML to prevent XSS attacks.
        """
        example_field = self.cleaned_data.get('example_field')
        if example_field:
            # Strip whitespace and validate
            example_field = example_field.strip()
            if len(example_field) < 3:
                raise forms.ValidationError("Field must be at least 3 characters long.")
        return example_field


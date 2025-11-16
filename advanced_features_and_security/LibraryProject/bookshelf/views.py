from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.html import escape
from .models import Book
from .forms import BookForm, BookSearchForm, ExampleForm


@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    """
    View to list all books. Requires can_view permission.
    
    Security: Uses Django ORM to prevent SQL injection.
    All user input is validated through forms before querying the database.
    """
    books = Book.objects.all()
    search_form = BookSearchForm(request.GET)
    
    # Secure search functionality using Django ORM (prevents SQL injection)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        if search_query:
            # Use Django ORM filter with Q objects - safe from SQL injection
            # Never use raw SQL or string formatting with user input!
            books = books.filter(
                Q(title__icontains=search_query) | 
                Q(author__icontains=search_query)
            )
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_form': search_form
    })


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """
    View to create a new book. Requires can_create permission.
    
    Security: Uses Django ModelForm to validate and sanitize all input.
    This prevents SQL injection and XSS attacks by:
    1. Validating input types and formats
    2. Escaping HTML automatically
    3. Using parameterized queries (Django ORM)
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Django ORM automatically uses parameterized queries
            # This prevents SQL injection attacks
            book = form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('bookshelf:list_books')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_create.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    """
    View to edit an existing book. Requires can_edit permission.
    
    Security: Uses Django ModelForm and get_object_or_404 for safe database access.
    Prevents SQL injection and ensures the book exists before editing.
    """
    book = get_object_or_404(Book, id=book_id)  # Safe - prevents invalid ID access
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # Django ORM handles all database operations safely
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('bookshelf:list_books')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_edit.html', {'form': form, 'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    """
    View to delete a book. Requires can_delete permission.
    
    Security: Uses get_object_or_404 and requires POST method.
    This prevents CSRF attacks (POST required) and ensures book exists.
    """
    book = get_object_or_404(Book, id=book_id)  # Safe database lookup
    
    if request.method == 'POST':
        # Only allow deletion via POST (CSRF protection)
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('bookshelf:list_books')
    
    return render(request, 'bookshelf/book_delete.html', {'book': book})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from .models import Book


@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    """
    View to list all books. Requires can_view permission.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """
    View to create a new book. Requires can_create permission.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        if title and author and publication_year:
            Book.objects.create(
                title=title,
                author=author,
                publication_year=int(publication_year)
            )
            messages.success(request, 'Book created successfully!')
            return redirect('bookshelf:list_books')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'bookshelf/book_create.html')


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    """
    View to edit an existing book. Requires can_edit permission.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        if title and author and publication_year:
            book.title = title
            book.author = author
            book.publication_year = int(publication_year)
            book.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('bookshelf:list_books')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'bookshelf/book_edit.html', {'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    """
    View to delete a book. Requires can_delete permission.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('bookshelf:list_books')
    
    return render(request, 'bookshelf/book_delete.html', {'book': book})

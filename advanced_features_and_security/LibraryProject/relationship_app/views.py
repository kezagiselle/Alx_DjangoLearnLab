from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Book, Library, UserProfile, Author


# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    Displays book titles and their authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    listing all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# User Authentication Views
class UserLoginView(LoginView):
    """
    Class-based view for user login using Django's built-in LoginView.
    """
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """
    Class-based view for user logout using Django's built-in LogoutView.
    """
    template_name = 'relationship_app/logout.html'


class UserRegisterView(CreateView):
    """
    Class-based view for user registration using Django's UserCreationForm.
    """
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('relationship_app:login')


# Function-based view for user registration
def register(request):
    """
    Function-based view for user registration using Django's UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Role-based access control helper functions
def is_admin(user):
    """
    Check if the user has the Admin role.
    """
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False


def is_librarian(user):
    """
    Check if the user has the Librarian role.
    """
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == 'Librarian'
    except UserProfile.DoesNotExist:
        return False


def is_member(user):
    """
    Check if the user has the Member role.
    """
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == 'Member'
    except UserProfile.DoesNotExist:
        return False


# Role-based views
@user_passes_test(is_admin, login_url='relationship_app:login')
def admin_view(request):
    """
    View accessible only to users with the Admin role.
    """
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian, login_url='relationship_app:login')
def librarian_view(request):
    """
    View accessible only to users with the Librarian role.
    """
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member, login_url='relationship_app:login')
def member_view(request):
    """
    View accessible only to users with the Member role.
    """
    return render(request, 'relationship_app/member_view.html')


# Book CRUD views with permission checks
@permission_required('relationship_app.can_add_book', login_url='relationship_app:login')
def add_book(request):
    """
    View to add a new book. Requires can_add_book permission.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('relationship_app:list_books')
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


@permission_required('relationship_app.can_change_book', login_url='relationship_app:login')
def edit_book(request, book_id):
    """
    View to edit an existing book. Requires can_change_book permission.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            book.title = title
            book.author = author
            book.save()
            return redirect('relationship_app:list_books')
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})


@permission_required('relationship_app.can_delete_book', login_url='relationship_app:login')
def delete_book(request, book_id):
    """
    View to delete a book. Requires can_delete_book permission.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})

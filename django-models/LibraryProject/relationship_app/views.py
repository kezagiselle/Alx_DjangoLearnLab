from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Book
from .models import Library


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

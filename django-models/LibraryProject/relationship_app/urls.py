from django.urls import path
from .views import list_books, UserLoginView, UserLogoutView, UserRegisterView
from relationship_app import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view: List all books
    path('books/', views.list_books, name='list_books'),
    # Class-based view: Library detail
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    # Authentication views
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
]


from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    View to list all books.
    Accessible to all users (read-only).
    Supports filtering by title, author, and publication_year.
    Supports searching by title and author name.
    Supports ordering by title and publication_year.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by ID.
    Accessible to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book.
    Restricted to authenticated users.
    Includes custom validation logic in the serializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic can be added here if needed
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Custom logic can be added here if needed
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

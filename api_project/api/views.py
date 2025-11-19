from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to list all books.
    Extends ListAPIView to provide a read-only endpoint for listing Book instances.
    
    Authentication: Requires token authentication (configured in settings.py)
    Permissions: Uses DEFAULT_PERMISSION_CLASSES from settings (IsAuthenticated)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Permission is inherited from REST_FRAMEWORK settings
    # Can override here if needed: permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling all CRUD operations on Book model.
    Provides actions for:
    - list: GET /books_all/ - List all books
    - create: POST /books_all/ - Create a new book
    - retrieve: GET /books_all/<id>/ - Retrieve a specific book
    - update: PUT /books_all/<id>/ - Update a book (full update)
    - partial_update: PATCH /books_all/<id>/ - Partially update a book
    - destroy: DELETE /books_all/<id>/ - Delete a book
    
    Authentication: Requires token authentication (configured in settings.py)
    Permissions: Uses DEFAULT_PERMISSION_CLASSES from settings (IsAuthenticated)
    
    To customize permissions, you can override:
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Permission is inherited from REST_FRAMEWORK settings
    # Default: IsAuthenticated (requires valid token)
    # Can override here for different permissions per viewset


from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to list all books.
    Extends ListAPIView to provide a read-only endpoint for listing Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library


# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    listing all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

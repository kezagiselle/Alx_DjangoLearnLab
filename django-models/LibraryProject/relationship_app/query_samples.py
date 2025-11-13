"""
Sample queries demonstrating Django ORM relationships:
- ForeignKey: Author -> Book
- ManyToMany: Library <-> Book
- OneToOne: Library -> Librarian
"""

from relationship_app.models import Author, Book, Library, Librarian


# 1. Query all books by a specific author (ForeignKey relationship)
def query_books_by_author(author_name):
    """
    Query all books by a specific author using ForeignKey relationship.
    
    Args:
        author_name (str): Name of the author
        
    Returns:
        QuerySet: All books by the specified author
    """
    # Get the author object first
    author = Author.objects.get(name=author_name)
    # Query all books by the author using filter(author=author)
    books = Book.objects.filter(author=author)
    
    return books


# 2. List all books in a library (ManyToMany relationship)
def list_books_in_library(library_name):
    """
    List all books in a library using ManyToMany relationship.
    
    Args:
        library_name (str): Name of the library
        
    Returns:
        QuerySet: All books in the specified library
    """
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    
    return books


# 3. Retrieve the librarian for a library (OneToOne relationship)
def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library using OneToOne relationship.
    
    Args:
        library_name (str): Name of the library
        
    Returns:
        Librarian: The librarian associated with the library
    """
    library = Library.objects.get(name=library_name)
    # Retrieve the librarian using Librarian.objects.get(library=library)
    librarian = Librarian.objects.get(library=library)
    
    return librarian


# Example usage function
def example_queries():
    """
    Example function demonstrating how to use the query functions.
    This creates sample data and runs the queries.
    """
    # Create sample data
    author1 = Author.objects.create(name="George Orwell")
    author2 = Author.objects.create(name="J.K. Rowling")

    book1 = Book.objects.create(title="1984", author=author1)
    book2 = Book.objects.create(title="Animal Farm", author=author1)
    book3 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author2)

    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="Community Library")

    # Add books to libraries (ManyToMany)
    library1.books.add(book1, book3)
    library2.books.add(book2)

    # Assign librarians (OneToOne)
    librarian1 = Librarian.objects.create(name="Alice", library=library1)
    librarian2 = Librarian.objects.create(name="Bob", library=library2)

    print("\n=== Query Results ===\n")

    # 1. Query all books by a specific author
    print("1. Books by George Orwell (ForeignKey):")
    books_by_author = query_books_by_author("George Orwell")
    for book in books_by_author:
        print(f"   - {book.title}")

    # 2. List all books in a library
    print("\n2. Books in Central Library (ManyToMany):")
    books_in_library = list_books_in_library("Central Library")
    for book in books_in_library:
        print(f"   - {book.title}")

    # 3. Retrieve the librarian for a library
    print("\n3. Librarian for Central Library (OneToOne):")
    librarian = retrieve_librarian_for_library("Central Library")
    print(f"   - {librarian.name}")


if __name__ == "__main__":
    # Note: This requires Django to be set up and migrations to be run
    # Run this from Django shell: python manage.py shell < relationship_app/query_samples.py
    # Or import and call: from relationship_app.query_samples import example_queries; example_queries()
    import os
    import django
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
    django.setup()
    
    example_queries()

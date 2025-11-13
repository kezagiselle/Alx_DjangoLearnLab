from relationship_app.models import Author, Book, Library, Librarian

def sample_queries():
    # Create sample data
    author1 = Author.objects.create(name="George Orwell")
    author2 = Author.objects.create(name="J.K. Rowling")

    book1 = Book.objects.create(title="1984", author=author1)
    book2 = Book.objects.create(title="Animal Farm", author=author1)
    book3 = Book.objects.create(title="Harry Potter", author=author2)

    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="Community Library")

    # Add books to libraries (ManyToMany)
    library1.books.add(book1, book3)
    library2.books.add(book2)

    # Assign librarians (OneToOne)
    librarian1 = Librarian.objects.create(name="Alice", library=library1)
    librarian2 = Librarian.objects.create(name="Bob", library=library2)

    print("\n--- Query Results ---")

    # 1️⃣ Query all books by a specific author
    author_books = Book.objects.filter(author__name="George Orwell")
    print("Books by George Orwell:")
    for book in author_books:
        print("-", book.title)

    # 2️⃣ List all books in a specific library
    library_books = library1.books.all()
    print(f"\nBooks in {library1.name}:")
    for book in library_books:
        print("-", book.title)

    # 3️⃣ Retrieve the librarian for a specific library
    librarian = library1.librarian
    print(f"\nLibrarian for {library1.name}: {librarian.name}")


if __name__ == "__main__":
    sample_queries()

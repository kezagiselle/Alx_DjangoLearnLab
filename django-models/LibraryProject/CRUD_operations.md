### Create
>>> from bookshelf.models import Book
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# Output: <Book: 1984 by George Orwell (1949)>

### Retrieve
>>> Book.objects.all()
# Output: [<Book: 1984 by George Orwell (1949)>]

### Update
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
# Output: <Book: Nineteen Eighty-Four by George Orwell (1949)>

### Delete
>>> book.delete()
# Output: (1, {'bookshelf.Book': 1})

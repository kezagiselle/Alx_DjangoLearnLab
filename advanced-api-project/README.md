# Advanced API Project

This project implements a Django REST Framework API for managing books and authors.

## API Endpoints

### Books

- **List Books**: `GET /api/books/`
    - Public access (read-only).
    - Supports filtering, searching, and ordering.
- **Retrieve Book**: `GET /api/books/<id>/`
    - Public access (read-only).
- **Create Book**: `POST /api/books/create/`
    - Authenticated users only.
- **Update Book**: `PUT /api/books/update/<id>/`
    - Authenticated users only.
- **Delete Book**: `DELETE /api/books/delete/<id>/`
    - Authenticated users only.

## Advanced Query Features

The `GET /api/books/` endpoint supports the following query parameters:

### Filtering
Filter books by exact matches:
- `title`: `?title=Book Title`
- `author`: `?author=1` (Author ID)
- `publication_year`: `?publication_year=2023`

### Searching
Search books by text (partial matches):
- `search`: `?search=query`
    - Searches in `title` and `author` name.

### Ordering
Order the results:
- `ordering`: `?ordering=field_name`
    - Fields: `title`, `publication_year`.
    - Ascending: `?ordering=title`
    - Descending: `?ordering=-title`

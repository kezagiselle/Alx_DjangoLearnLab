# Django REST Framework API Project

This is a Django project set up specifically for building APIs using Django REST Framework.

## Project Structure

```
api_project/
├── api_project/          # Project settings
│   ├── __init__.py
│   ├── settings.py       # Django settings (includes rest_framework)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── api/                  # API app
│   ├── __init__.py
│   ├── models.py        # Book model defined here
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   └── migrations/       # Database migrations
├── manage.py
└── db.sqlite3            # SQLite database (created after migrations)
```

## Setup Complete

✅ Django project created (`api_project`)
✅ Django REST Framework installed and configured
✅ API app created (`api`)
✅ Book model created with `title` and `author` fields
✅ Migrations created

## Installation Requirements

To use this project, you need to install:

```bash
pip install django
pip install djangorestframework
```

## Configuration

### INSTALLED_APPS

The following apps are configured in `settings.py`:

- `rest_framework` - Django REST Framework
- `api` - The API application

### Model

The `Book` model is defined in `api/models.py`:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
```

## Running Migrations

To set up the database, run:

```bash
python manage.py migrate
```

This will create the database tables for the Book model.

## Starting the Development Server

To start the Django development server:

```bash
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/` to confirm the server is running.

## Next Steps

This project is now ready for:
- Creating API serializers
- Building API views and viewsets
- Setting up API endpoints
- Implementing authentication and permissions


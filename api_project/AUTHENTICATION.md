# API Authentication and Permissions Guide

This document explains how authentication and permissions are configured in the Django REST Framework API.

## Overview

The API uses **Token Authentication** to secure endpoints. Users must obtain an authentication token and include it in their requests to access protected endpoints.

## Authentication Setup

### 1. Token Authentication Configuration

Token authentication is configured in `api_project/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',  # Token authentication for API
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # For browsable API
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### 2. Database Migration

After adding `rest_framework.authtoken` to INSTALLED_APPS, run:

```bash
python manage.py migrate
```

This creates the `authtoken_token` table for storing user tokens.

## Obtaining an Authentication Token

### Endpoint: `/api/api-token-auth/`

**Method:** POST

**Request Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Example using curl:

```bash
curl -X POST http://127.0.0.1:8000/api/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Example using Postman:

1. Set method to POST
2. URL: `http://127.0.0.1:8000/api/api-token-auth/`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```

## Using the Token in API Requests

Once you have a token, include it in the `Authorization` header of all API requests:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Example using curl:

```bash
curl http://127.0.0.1:8000/api/books_all/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Example using Postman:

1. Go to the **Authorization** tab
2. Select **Type: Token**
3. Enter your token in the **Token** field
4. Or manually add header: `Authorization: Token your_token_here`

## Permissions

### Default Permission: IsAuthenticated

All API endpoints require authentication by default. This is configured in `settings.py`:

```python
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
],
```

### Available Permission Classes

DRF provides several built-in permission classes:

- **IsAuthenticated**: User must be authenticated (default)
- **IsAdminUser**: User must be a staff/admin user
- **IsAuthenticatedOrReadOnly**: Read access for all, write requires authentication
- **AllowAny**: No authentication required (not recommended for production)
- **DjangoModelPermissions**: Uses Django's permission system

### Customizing Permissions

You can override permissions per view/viewset:

```python
from rest_framework import permissions

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Override default permissions
    permission_classes = [permissions.IsAdminUser]  # Only admins can access
```

## Protected Endpoints

All endpoints require authentication:

### BookList View:
- `GET /api/books/` - Requires token

### BookViewSet:
- `GET /api/books_all/` - List all books (requires token)
- `POST /api/books_all/` - Create a book (requires token)
- `GET /api/books_all/<id>/` - Retrieve a book (requires token)
- `PUT /api/books_all/<id>/` - Update a book (requires token)
- `PATCH /api/books_all/<id>/` - Partially update (requires token)
- `DELETE /api/books_all/<id>/` - Delete a book (requires token)

## Testing Authentication

### 1. Test Without Token (Should Fail)

```bash
curl http://127.0.0.1:8000/api/books_all/
```

**Expected Response:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 2. Obtain Token

```bash
curl -X POST http://127.0.0.1:8000/api/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

### 3. Test With Token (Should Succeed)

```bash
curl http://127.0.0.1:8000/api/books_all/ \
  -H "Authorization: Token your_token_here"
```

**Expected Response:**
```json
[]
```

### 4. Create a Book with Token

```bash
curl -X POST http://127.0.0.1:8000/api/books_all/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "author": "Test Author"}'
```

## Creating Test Users

To test authentication, create a user:

### Using Django Shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
user = User.objects.create_user('testuser', 'test@example.com', 'testpass')
```

### Using Django Admin:

1. Create a superuser: `python manage.py createsuperuser`
2. Log in to admin: `http://127.0.0.1:8000/admin/`
3. Create a user in the Users section

## Security Best Practices

1. **Always use HTTPS in production** - Tokens should never be sent over unencrypted connections
2. **Store tokens securely** - Never commit tokens to version control
3. **Rotate tokens regularly** - Consider implementing token expiration
4. **Use strong passwords** - Enforce password complexity requirements
5. **Limit token scope** - Consider implementing different permission levels
6. **Monitor token usage** - Log authentication attempts and failures

## Troubleshooting

### Issue: "Authentication credentials were not provided"

**Solution:** Include the token in the Authorization header:
```
Authorization: Token your_token_here
```

### Issue: "Invalid token"

**Solution:** 
- Verify the token is correct
- Check if the token exists in the database
- Generate a new token if needed

### Issue: Token endpoint returns 400 Bad Request

**Solution:**
- Verify username and password are correct
- Ensure Content-Type header is set to `application/json`
- Check that the user account is active

## Additional Resources

- [DRF Authentication Documentation](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
- [DRF Permissions Documentation](https://www.django-rest-framework.org/api-guide/permissions/)
- [DRF Token Authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)


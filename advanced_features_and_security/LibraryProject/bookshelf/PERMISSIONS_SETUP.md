# Groups and Permissions Setup Guide

This document explains how to set up and use the groups and permissions system in the Django application.

## Overview

The application uses Django's built-in groups and permissions system to control access to book-related operations. Custom permissions have been defined in the `Book` model to restrict actions such as viewing, creating, editing, and deleting books.

## Custom Permissions

The following custom permissions are defined in the `Book` model:

- **can_view**: Allows users to view the list of books
- **can_create**: Allows users to create new books
- **can_edit**: Allows users to edit existing books
- **can_delete**: Allows users to delete books

These permissions are defined in `bookshelf/models.py`:

```python
class Meta:
    permissions = [
        ('can_view', 'Can view book'),
        ('can_create', 'Can create book'),
        ('can_edit', 'Can edit book'),
        ('can_delete', 'Can delete book'),
    ]
```

## Setting Up Groups

### Step 1: Access Django Admin

1. Start the Django development server: `python manage.py runserver`
2. Navigate to `http://localhost:8000/admin/`
3. Log in with a superuser account

### Step 2: Create Groups

1. Go to **Authentication and Authorization** → **Groups**
2. Click **Add Group** and create the following groups:

#### Viewers Group
- **Name**: Viewers
- **Permissions**: 
  - bookshelf | book | Can view book

#### Editors Group
- **Name**: Editors
- **Permissions**:
  - bookshelf | book | Can view book
  - bookshelf | book | Can create book
  - bookshelf | book | Can edit book

#### Admins Group
- **Name**: Admins
- **Permissions**:
  - bookshelf | book | Can view book
  - bookshelf | book | Can create book
  - bookshelf | book | Can edit book
  - bookshelf | book | Can delete book

### Step 3: Assign Users to Groups

1. Go to **Authentication and Authorization** → **Users** (or **Custom Users**)
2. Select a user
3. Scroll to the **Groups** section
4. Add the user to the appropriate group(s)
5. Save the user

## Permission Enforcement in Views

All views in `bookshelf/views.py` are protected with the `@permission_required` decorator:

- `list_books()` - Requires `bookshelf.can_view`
- `create_book()` - Requires `bookshelf.can_create`
- `edit_book()` - Requires `bookshelf.can_edit`
- `delete_book()` - Requires `bookshelf.can_delete`

Example:
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # View implementation
```

The `raise_exception=True` parameter causes a 403 Forbidden error if the user doesn't have the required permission.

## Testing Permissions

### Step 1: Create Test Users

1. Create three test users in Django admin:
   - `viewer_user` - Assign to Viewers group
   - `editor_user` - Assign to Editors group
   - `admin_user` - Assign to Admins group

### Step 2: Test Access

1. Log in as `viewer_user`:
   - ✅ Should be able to view books list
   - ❌ Should NOT be able to create, edit, or delete books

2. Log in as `editor_user`:
   - ✅ Should be able to view books list
   - ✅ Should be able to create books
   - ✅ Should be able to edit books
   - ❌ Should NOT be able to delete books

3. Log in as `admin_user`:
   - ✅ Should be able to perform all operations (view, create, edit, delete)

### Step 3: Verify Permission Errors

When a user without the required permission tries to access a protected view, they will receive a 403 Forbidden error.

## URL Patterns

The following URLs are available:

- `/bookshelf/` - List all books (requires `can_view`)
- `/bookshelf/create/` - Create a new book (requires `can_create`)
- `/bookshelf/edit/<book_id>/` - Edit a book (requires `can_edit`)
- `/bookshelf/delete/<book_id>/` - Delete a book (requires `can_delete`)

## Important Notes

1. **Run Migrations**: After adding custom permissions to the model, run:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Superusers**: Superusers automatically have all permissions and can bypass permission checks.

3. **Permission Format**: Permissions follow the format `app_name.permission_name` (e.g., `bookshelf.can_view`).

4. **Groups vs Individual Permissions**: You can assign permissions directly to users or assign users to groups. Groups make it easier to manage permissions for multiple users.

## Troubleshooting

- If permissions don't appear in the admin, ensure migrations have been run
- If users can't access views, verify they are assigned to the correct group or have the required permission
- Check that the user is logged in (permission checks require authentication)
- Verify the permission name matches exactly (case-sensitive)


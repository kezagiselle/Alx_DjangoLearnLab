from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Author
from django.contrib.auth.models import User
from datetime import datetime

class BookAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", publication_year=2023, author=self.author)

    def test_list_books(self):
        url = '/api/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_book(self):
        url = f'/api/books/{self.book.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book")

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        url = '/api/books/create/'
        data = {
            "title": "New Book",
            "publication_year": 2024,
            "author": self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        url = '/api/books/create/'
        data = {
            "title": "New Book",
            "publication_year": 2024,
            "author": self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        url = f'/api/books/update/{self.book.id}/'
        data = {
            "title": "Updated Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_update_book_unauthenticated(self):
        url = f'/api/books/update/{self.book.id}/'
        data = {
            "title": "Updated Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        url = f'/api/books/delete/{self.book.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):
        url = f'/api/books/delete/{self.book.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

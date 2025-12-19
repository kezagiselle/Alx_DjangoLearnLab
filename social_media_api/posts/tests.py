from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class PostAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client.force_authenticate(user=self.user1)
        self.post1 = Post.objects.create(author=self.user1, title='First Post', content='Content of first post')
        self.post2 = Post.objects.create(author=self.user2, title='Second Post', content='Content of second post')
        self.create_url = reverse('post-list')

    def test_create_post(self):
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(Post.objects.get(id=response.data['id']).author, self.user1)

    def test_update_post(self):
        url = reverse('post-detail', args=[self.post1.id])
        data = {'title': 'Updated Title', 'content': 'Updated Content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Title')

    def test_update_post_not_author(self):
        url = reverse('post-detail', args=[self.post2.id])
        data = {'title': 'Updated Title'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post(self):
        url = reverse('post-detail', args=[self.post1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_not_author(self):
        url = reverse('post-detail', args=[self.post2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_posts(self):
        response = self.client.get(self.create_url, {'search': 'First'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'First Post')

class CommentAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.post = Post.objects.create(author=self.user1, title='Post', content='Content')
        self.client.force_authenticate(user=self.user1)
        self.comment_url = reverse('comment-list')

    def test_create_comment(self):
        data = {'post': self.post.id, 'content': 'Nice post!'}
        response = self.client.post(self.comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().author, self.user1)

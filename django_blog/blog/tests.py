from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', email='test@example.com')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/register.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/login.html')

    def test_login_functionality(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertRedirects(response, reverse('profile'))

    def test_profile_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/profile.html')

    def test_profile_update(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('profile'), {'username': 'testuser', 'email': 'newemail@example.com'})
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_logout_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/logout.html')

from .models import Post

class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_list_view(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post-create'), {'title': 'New Post', 'content': 'New Content'})
        self.assertRedirects(response, reverse('post-detail', kwargs={'pk': 2}))
        self.assertEqual(Post.objects.count(), 2)

    def test_post_update_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post-update', kwargs={'pk': self.post.pk}), {'title': 'Updated Post', 'content': 'Updated Content'})
        self.assertRedirects(response, reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertRedirects(response, '/')
        self.assertEqual(Post.objects.count(), 0)

    def test_post_update_view_forbidden(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.post(reverse('post-update', kwargs={'pk': self.post.pk}), {'title': 'Updated Post', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 403)

    def test_post_delete_view_forbidden(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)

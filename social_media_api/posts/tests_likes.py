from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikeDataTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client.force_authenticate(user=self.user1)
        self.post = Post.objects.create(author=self.user2, title='Test Post', content='Content')
        self.like_url = reverse('like_post', args=[self.post.id])
        self.unlike_url = reverse('unlike_post', args=[self.post.id])

    def test_like_post(self):
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 1)
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post).exists())
        
        # Check notification
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.get()
        self.assertEqual(notification.recipient, self.user2)
        self.assertEqual(notification.actor, self.user1)
        self.assertEqual(notification.verb, 'liked')

    def test_unlike_post(self):
        Like.objects.create(user=self.user1, post=self.post)
        response = self.client.post(self.unlike_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

    def test_like_existing_post(self):
        Like.objects.create(user=self.user1, post=self.post)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Should not create another notification? Implementation does get_or_create
        # Logic: if created: make notification. So no new notification.
        # But previous manually created Like didn't create notification (unless done via view).
        # Count should remain 0 notifications because Like was created manually in setup without notif.
        self.assertEqual(Notification.objects.count(), 0)

class NotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.actor = User.objects.create_user(username='actor', password='password')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('notification_list')
        
        self.notification = Notification.objects.create(
            recipient=self.user,
            actor=self.actor,
            verb='tested',
            target=self.actor # Just using actor as target compliant with any model
        )

    def test_get_notifications(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['verb'], 'tested')

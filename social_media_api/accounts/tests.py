from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        url = reverse('follow_user', args=[self.user2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if user1 is following user2
        # Since related_name='followers', user2.followers should include user1
        # And user1.following should include user2
        self.assertTrue(self.user2 in self.user1.following.all())

    def test_unfollow_user(self):
        self.user1.following.add(self.user2)
        url = reverse('unfollow_user', args=[self.user2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user2 in self.user1.following.all())

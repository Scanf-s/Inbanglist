import time
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core import mail


class UserRegisterAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user_register')
        self.user1 = {
            'email': 'calzone0404@gmail.com',
            'password': '123456',
            'password_verify': '123456'
        }
        self.user2 = {
            'email': 'sullung2yo@gmail.com',
            'password': '123456',
            'password_verify': '123456'
        }

    def test_register_multiple_users(self):
        start_time = time.time()

        # Register first user
        response1 = self.client.post(self.url, self.user1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response1.data)
        self.assertEqual(response1.data['user']['email'], self.user1['email'])

        # Register second user
        response2 = self.client.post(self.url, self.user2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response2.data)
        self.assertEqual(response2.data['user']['email'], self.user2['email'])

        end_time = time.time()
        total_time = end_time - start_time

        print(f"Total time for registering two users: {total_time:.2f} seconds")

        self.assertEqual(len(mail.outbox), 2)

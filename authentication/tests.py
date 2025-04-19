from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterTest(APITestCase):
    def setUp(self):
        self.url = reverse('register')
        self.data = {
            'username': 'test_user',
            'password': '34qwerty1234'
        }

    def test_create_account(self):
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['username'], self.data['username'])

    def test_create_account_without_password(self):
        response = self.client.post(self.url, self.data.get('username'), format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_duplicate_username(self):
        User.objects.create_user(username='test_user', password='qwerty1234')
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_weak_password(self):
        data = {'username': 'test_user', 'password': '123'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_not_in_response(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertNotIn('password', response.data)


class JWTAuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='34qwerty1234')
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.verify_url = reverse('token_verify')
        self.data = {
            'username': 'test_user',
            'password': '34qwerty1234'
        }

    def test_token_obtain_pair(self):
        response = self.client.post(self.token_url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        response = self.client.post(self.token_url, self.data, format='json')
        refresh_token = response.data['refresh']
        response = self.client.post(self.refresh_url, {'refresh': refresh_token}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_verify(self):
        response = self.client.post(self.token_url, self.data, format='json')
        access_token = response.data['access']
        response = self.client.post(self.verify_url, {'token': access_token}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

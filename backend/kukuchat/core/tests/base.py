from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class AuthenticatedTestCase(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username='test',
            password='test',
            email='test@test.test'
        )
        token = Token.objects.create(user=user).key
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')


from django.test import TestCase 
from django.contrib.auth import get_user_model


class AuthTestCase(TestCase):
    def test_user_register(self):
        user = self.client.post('/api/register/',{'username': 'user1','password': '12qwertyU','email': 'user1@yopmail.com'})
        self.assertEqual(1, get_user_model().objects.all().count())
        results = get_user_model().objects.all().values('username', 'password', 'email')
        results = list(results)
        self.assertListEqual(results, [{'username': 'user1', 'password': '12qwertyU','email': 'user1@yopmail.com'}])

    def test_user_login(self):
        get_user_model().objects.create_user(username='user1', password='12qwertyU', email='user1@yopmail.com')
        response = self.client.post('/api/login/',{'username': 'user1','password': '12qwertyU'})
        self.assertIn('token', response.json())

        
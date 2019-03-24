import json
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from core.tests import base
from core.providers import facebook, telegram


class ProvidersTests(base.AuthenticatedTestCase):

    def setUp(self):
        super().setUp()

    def test_can_list_avaliable_providers(self):
        resp = self.client.get('/api/provider/get_avaliable_providers/')
        self.assertDictEqual(
            resp.json(),
            {
                'providers': [
                    {
                        'name': 'telegram',
                        'credentials': telegram.TelegramProvider.get_required_credentials(),
                    },
                    {
                        'name': 'facebook',
                        'credentials': facebook.FacebookProvider.get_required_credentials(),
                    }
                ],
            },
        )


    def test_can_login_into_messenger(self):
        resp = self.client.post(
            '/api/provider/facebook/login/',
            {
                'username': '579631148',
                'password': '12qwertyU',
            },
            format='json',
        )
        self.assertTrue(facebook.FacebookProvider.client)
        self.assertEqual(200, resp.status_code)

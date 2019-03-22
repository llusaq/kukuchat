from unittest.mock import patch

from django.test import TestCase

import fbchat

from core.providers.facebook import FacebookProvider


class FacebookTests(TestCase):

    @patch.object(fbchat, 'Client')
    def test_can_login(self, client_mock):
        pass

from unittest.mock import patch

from django.test import TestCase

from telethon import TelegramClient, sync

from core.providers.telegram import TelegramProvider

class TelegramTests(TestCase):

    @patch.object(TelegramClient, 'TelegramClient')
    def test_can_login(self, client_mock):
        TelegramProvider.login()
        print (abc)
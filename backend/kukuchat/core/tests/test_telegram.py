from unittest.mock import patch

from django.test import TestCase

from telethon import TelegramClient, sync

from core.providers.telegram import TelegramProvider

class TelegramTests(TestCase):

    def test_can_login(self):
        TelegramProvider.login()
from core.providers.provider import BaseProvider
from core.models import Contact, Chat
from core import utils
from telethon import TelegramClient, sync

from channels.db import database_sync_to_async

from asgiref.sync import sync_to_async


class TelegramProvider(BaseProvider):

    name = 'telegram'

    _required_credentials = {
        #'username': {'type': 'text', 'help': 'Unique username or phone number'},
    }

    def __init__(self, scope):
      self.client = None

    async def get_required_credentials(self):
        return self._required_credentials

    async def login(self, data):
        import ipdb; ipdb.set_trace()
        apiid = '873144'
        apihash = 'd7f230abfc4ec30c8323fa5fd2223161'
        self.client = TelegramClient('telegram_session', apiid, apihash)
        await self.client.start()
        #import ipdb; ipdb.set_trace()

        return {'msg': 'Succesfully logged into Telegram'}

    async def am_i_logged(self, data):
        is_logged = self.client is not None
        return {'is_logged': is_logged}

    async def get_chats(self, data):
        pass

    async def post_login_action(self, data):
        pass

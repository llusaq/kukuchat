from core.providers.provider import BaseProvider
from core.models import Contact, Chat
from core import utils
from pyrogram import Client

from channels.db import database_sync_to_async

from asgiref.sync import sync_to_async, async_to_sync

from pathlib import Path
import tempfile
from datetime import datetime

from channels.auth import get_user
from threading import Thread

from skpy import SkypeNewMessageEvent


class TelegramProvider(BaseProvider):

    name = 'telegram'

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Unique username or phone number'},
    }

    def __init__(self, scope):
      self.client = None
      self.scope = scope
      self.user = None

    async def get_required_credentials(self):
        return self._required_credentials

    async def login(self, data):
        #import ipdb; ipdb.set_trace()
        phone = '+48609523405'
        apiid = '873144'
        apihash = 'd7f230abfc4ec30c8323fa5fd2223161'
        #self.user = await get_user(self.scope)

        #temp = tempfile.gettempdir() / Path(self.user.temp_dir)
       # self._token_path = str(temp / 'token_telegram_app')
        #import ipdb; ipdb.set_trace()
        self.client = Client("telegram_session", apiid, apihash)
        await self.client.start()
        print("abcd")
        return {'msg': 'Succesfully logged into Telegram'}

    async def am_i_logged(self, data):
        #import ipdb; ipdb.set_trace()
        is_logged = self.client is not None and (await self.client.get_me()).is_self
        return {'is_logged': is_logged}

    async def get_chats(self, data):
        all_contacts = self.client.get_contacts()
        active_contacts = [c for c in all_contacts if c.id]
        chats = await utils.turn_provider_contacts_into_chats(
            active_contacts,
            lambda c: c.id,
            lambda c: c.first_name,
            'telegram',
        )
        return {'chats': [{'id': c.id, 'name': c.first_name} for c in chats]}

    async def post_login_action(self, data):
        pass
import logging
from pathlib import Path
import tempfile 

from channels.auth import get_user
from threading import Thread


from skpy import Skype
from skpy import SkypeAuthException

from asgiref.sync import sync_to_async, async_to_sync

from core.providers.provider import BaseProvider
from core import utils



class SkypeProvider(BaseProvider):

    name = 'skype'

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'},
    }

    def __init__(self, scope):
        self.sk = Skype(connect=False)
        self.scope = scope
        self.on_message_consumer = on_message_consumer

    async def get_required_credentials(self, data):
        return self._required_credentials

    async def login(self, data):
        username = data['username']
        password = data['password']

        user_self = await get_user(self.scope)
        temp = tempfile.gettempdir() / Path(user_self.temp_dir) 
        self.sk.conn.setTokenFile(temp / "token-skype-app")
        try:
            self.sk.conn.readToken()
        except SkypeAuthException:
            self.sk.conn.setUserPwd(username, password)
            self.sk.conn.getSkypeToken()
            


        return {'msg': 'Successfully logged into Skype'}

    async def am_i_logged(self, data):
        is_logged = self.sk.conn.connected is True
        return {'is_logged': is_logged}

    async def get_chats(self, data):
        all_contacts = self.sk.contacts
        active_contacts = [c for c in all_contacts if c.id]
        chats = await utils.turn_provider_contacts_into_chats(
            active_contacts,
            lambda c: c.id,
            lambda c: c.name.first + c.name.last,
            'skype'
        )
        return {'chats': [{'id': c.id, 'name': c.name} for c in chats]}
    async def post_login_action(self, data):
        pass
    def on_message(self, *args, **kwargs):
        t = Thread(
            target=async_to_sync(self.on_message_consumer),
            kwargs={
                'provider': 'skype',
                'author_uid': kwargs['author_id'],
                'content': kwargs['message_object'].text,
                'author_name': kwargs['name'],
            }
        )
        t.start()

    async def send_message(self, id, content):
        ch = self.sk.chats[id]
        await sync_to_async(ch.sendMsg)(content)
        return {'provider': 'skype'}

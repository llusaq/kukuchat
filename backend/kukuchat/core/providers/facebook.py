from multiprocessing import Process

import fbchat
from fbchat.models import Message

from asgiref.sync import sync_to_async

from core.providers.provider import BaseProvider
from core import utils


class FacebookProvider(BaseProvider):

    name = 'facebook'

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'},
    }

    def __init__(self, scope):
        self.client = None

    async def get_required_credentials(self, data):
        return self._required_credentials

    async def login(self, data):
        username = data['username']
        password = data['password']

        self.client = fbchat.Client(username, password)
        self.listener = Process(target=lambda: self.client.listen(markAlive=True))
        self.listener.start()

        return {'msg': 'Successfuly logged into Facebook'}

    async def am_i_logged(self, data):
        is_logged = self.client is not None and self.client.isLoggedIn()
        return {'is_logged': is_logged}

    async def get_chats(self, data):
        all_contacts = await sync_to_async(self.client.fetchAllUsers)()
        active_contacts = [c for c in all_contacts if c.uid]
        chats = await utils.turn_provider_contacts_into_chats(
            active_contacts,
            lambda c: c.uid,
            lambda c: c.name,
            'facebook',
        )
        return {'chats': [{'id': c.id, 'name': c.name} for c in chats]}

    async def post_login_action(self, data):
        pass

    async def send_message(self, uid, content):
        await sync_to_async(self.client.send)(Message(text=content), uid)
        return {'provider': 'facebook'}

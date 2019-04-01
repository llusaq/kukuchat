import logging

import fbchat

from asgiref.sync import sync_to_async

from core.providers.provider import BaseProvider


class FacebookProvider(BaseProvider):

    name = 'facebook'

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'},
    }

    def __init__(self, user):
        self.client = None

    async def get_required_credentials(self, data):
        return self._required_credentials

    async def login(self, data):
        username = data['username']
        password = data['password']

        self.client = fbchat.Client(username, password)

        return {'msg': 'Successfuly logged into Facebook'}

    async def am_i_logged(self, data):
        is_logged = self.client is not None and self.client.isLoggedIn()
        return {'is_logged': is_logged}

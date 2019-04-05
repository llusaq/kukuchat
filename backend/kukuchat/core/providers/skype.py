import logging

from skpy import Skype

from skpy import SkypeAuthException


from asgiref.sync import sync_to_async

from core.providers.provider import BaseProvider


class SkypeProvider(BaseProvider):

    name = 'skype'

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'},
    }

    def __init__(self, scope):
        self.sk = Skype(connect=False)
        self.scope = scope

    async def get_required_credentials(self, data):
        return self._required_credentials

    async def login(self, data):
        username = data['username']
        password = data['password']

        self.sk.conn
        self.sk.conn.setTokenFile(".token-skype-app")
        try:
            self.sk.conn.readToken()
        except SkypeAuthException:
            self.sk.conn.setUserPwd(username, password)
            await sync_to_async(self.sk.conn.getSkypeToken)()

        return {'msg': 'Successfully logged into Skype'}

    async def am_i_logged(self, data):
        is_logged = self.sk.conn.connected is True
        return {'is_logged': is_logged}

    async def get_chats(self, data):
        pass

    async def post_login_action(self, data):
        pass

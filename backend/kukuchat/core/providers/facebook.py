import fbchat

from core.providers.provider import BaseProvider


class FacebookProvider(BaseProvider):

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'},
    }


    def __init__(self):
        self.client = None

    def get_required_credentials(self):
        return self._required_credentials

    def login(self, **credentials):
        username = credentials['username']
        password = credentials['password']

        self.client = fbchat.Client(username, password)

    def is_logged_in(self):
        return self.client is None and self.client.isLoggedIn()

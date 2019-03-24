import fbchat

from core.providers.provider import BaseProvider


class FacebookProvider(BaseProvider):

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'},
    }

    client = None

    @classmethod
    def get_required_credentials(cls):
        return cls._required_credentials

    @classmethod
    def login(cls, **credentials):
        username = credentials['username']
        password = credentials['password']

        cls.client = fbchat.Client(username, password)

from core.providers.provider import BaseProvider
from telethon import TelegramClient


class TelegramProvider(BaseProvider):

    _required_credentials = {
        'phone_number': {'type': 'text', 'help': 'Phone number'},
        'api_id': {'type': 'number', 'help': 'Api ID'},
        'api_hash': {'type': 'text', 'help': 'Api hash'},
    }

    def __init__(self, scope):
        self.Client = None

    async def get_required_credentials(self):
        return self._required_credentials

    async def login(self, data):
        apiid = data['api_id']
        apihash = data['api_hash']
        self.Client = TelegramClient('telegram_session', apiid, apihash).start()

        return {'msg': 'Succesfully logged into Telegram'}

    async def is_logged_in(self):
        pass

    async def post_login_action(self, data):
        pass

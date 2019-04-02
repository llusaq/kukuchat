from core.providers.provider import BaseProvider


class TelegramProvider(BaseProvider):

    _required_credentials = {
        'phone_number': {'type': 'text', 'help': 'Phone number'},
        'api_id': {'type': 'number', 'help': 'Api ID'},
        'api_hash': {'type': 'text', 'help': 'Api hash'},
    }

    def __init__(self, scope):
        self.Client = None

    def get_required_credentials(self):
        return self._required_credentials

    def login(self, **credentials):
        pass

    def is_logged_in(self):
        pass

    async def post_login_action(self, data):
        pass

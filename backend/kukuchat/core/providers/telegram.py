from core.providers.provider import BaseProvider


class TelegramProvider(BaseProvider):

    _required_credentials = {
        'phone_number': {'type': 'text', 'help': 'Phone number'},
        'api_id': {'type': 'number', 'help': 'Api ID'},
        'api_hash': {'type': 'text', 'help': 'Api hash'},
    }

    client = None

    @classmethod
    def get_required_credentials(cls):
        return cls._required_credentials

    @classmethod
    def login(cls, **credentials):
        pass

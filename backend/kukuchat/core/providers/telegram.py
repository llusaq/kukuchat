from telethon import TelegramClient, sync

from core.providers.provider import BaseProvider

class TelegramProvider(BaseProvider):

    _required_credentials = {
        'phone_number': {'type': 'text', 'help': 'Phone number'},
        'api_id': {'type': 'number', 'help': 'Api ID'},
        'api_hash': {'type': 'text', 'help': 'Api hash'},
    }

    @classmethod
    def get_required_credentials(cls):
        return cls._required_credentials

    @classmethod
    def login(cls, **credentials):
        phone_number = cls._required_credentials['phone_number']
        api_id = cls._required_credentials['api_id']
        api_hash = cls.required_credentials['api_hash']

        client = cls.TelegramClient('Telegram_cli', api_id, api_hash)
        client.start()
        me = client.get_me()
        me.send_message('medford', 'Test message')

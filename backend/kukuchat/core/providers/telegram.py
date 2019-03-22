from telethon import TelegramClient, sync

class TelegramProvider:

    _required_credentials = {
        'phone_number': '123123123'
        'api_id': 873144
        'api_hash': 'd7f230abfc4ec30c8323fa5fd2223161'
    }


    @classmethod
    def login (cls, **_required_credentials):
        phone_number = _required_credentials['phone_number']
        api_id = _required_credentials['api_id']
        api_hash = _required_credentials['api_hash']

        client = cls.TelegramClient(Telegram_cli, api_id, api_hash)
        client.start()
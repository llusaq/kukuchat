from telethon import TelegramClient, sync

class TelegramProvider:

    @classmethod
    def login (cls, **credentials):
        phone_number = 123123123
        api_id = 873144
        api_hash = 'd7f230abfc4ec30c8323fa5fd2223161'

        client = TelegramClient('Telegram_cli', api_id, api_hash)
        client.start()
        client.send_message('medford', 'Hi there')

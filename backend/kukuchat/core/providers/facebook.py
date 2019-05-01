import fbchat
from fbchat.models import Message

from core.providers.provider import BaseProvider
from core import utils


class FacebookProvider(BaseProvider):

    name = 'facebook'

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'},
    }

    def __init__(self, scope, on_message_consumer):
        self.on_message_consumer = on_message_consumer
        self.client = None

    async def get_required_credentials(self, data):
        return self._required_credentials

    async def login(self, data):
        username = data['username']
        password = data['password']

        self.client = fbchat.Client()
        await self.client.start(username, password)
        self.client.onMessage = self.on_message
        self.client.listen(markAlive=True)

        return {'msg': 'Successfuly logged into Facebook'}

    async def am_i_logged(self, data):
        is_logged = self.client is not None and self.client.isLoggedIn()
        return {'is_logged': is_logged}

    async def get_chats(self, data):
        all_contacts = await self.client.fetchAllUsers()
        active_contacts = [c for c in all_contacts if c.uid]
        chats = await utils.turn_provider_contacts_into_chats(
            active_contacts,
            lambda c: c.uid,
            lambda c: c.name,
            'facebook',
        )
        return {'chats': [{'id': c.id, 'name': c.name} for c in chats]}

    async def post_login_action(self, data):
        pass

    async def on_message(self, *args, **kwargs):
        aid = kwargs['author_id']
        user = (await self.client.fetchUserInfo(aid))[aid]
        await self.on_message_consumer(
            provider='facebook',
            author_uid=kwargs['author_id'],
            content=kwargs['message_object'].text,
            author_name=user.name,
        )

    async def send_message(self, uid, content):
        await self.client.send(Message(text=content), uid)
        return {'provider': 'facebook'}

    async def get_last_messages(self, uid, count):
        msgs = await self.client.fetchThreadMessages(uid, limit=count)
        msgs = [{'provider': 'facebook', 'content': m.text} for m in msgs]
        return msgs

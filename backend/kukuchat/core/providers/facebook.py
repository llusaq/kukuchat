from datetime import datetime
import pytz

import fbchat
from fbchat.models import Message, ThreadType

from channels.auth import get_user

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
        self.scope = scope
        self.client = None

    async def get_required_credentials(self, data):
        return self._required_credentials

    async def login(self, data):
        username = data['username']
        password = data['password']

        self.client = fbchat.Client(
            user_agent=(
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3)'
                'AppleWebKit/601.1.10 (KHTML, like Gecko    )'
                'Version/8.0.5 Safari/601.1.10'
            )
        )
        await self.client.start(username, password)
        self.client.onMessage = self._on_message
        self.client.listen(markAlive=True)

        return {'msg': 'Successfuly logged into Facebook'}

    async def am_i_logged(self, data):
        is_logged = self.client is not None and await self.client.isLoggedIn()
        return {'is_logged': is_logged}

    async def post_login_action(self, data):
        pass

    async def get_chats(self, data):
        all_contacts = await self.client.fetchAllUsers()
        active_contacts = [c for c in all_contacts if c.uid]
        chats = await utils.turn_provider_contacts_into_chats(
            active_contacts,
            lambda c: c.uid,
            lambda c: c.name,
            'facebook',
            user=await get_user(self.scope),
        )
        return {'chats': [{'id': c.id, 'name': c.name} for c in chats]}

    async def _on_message(self, *args, **kwargs):
        if kwargs['thread_type'] != ThreadType.USER:
            return
        aid = kwargs['author_id']
        user = (await self.client.fetchUserInfo(aid))[aid]
        ts = str(kwargs['message_object'].timestamp)[:-3]
        time = datetime.utcfromtimestamp(int(ts)).replace(tzinfo=pytz.UTC)
        await self.on_message_consumer(
            provider='facebook',
            author_uid=kwargs['author_id'],
            content=kwargs['message_object'].text,
            author_name=user.name,
            time=time,
        )

    async def send_message(self, uid, content):
        await self.client.send(Message(text=content), uid)
        return {'provider': 'facebook'}

    async def get_last_messages(self, uid, count):
        msgs = await self.client.fetchThreadMessages(uid, limit=count)
        msgs = [
            {
                'provider': 'facebook',
                'content': m.text,
                'me': m.author == self.client.uid,
                'time': datetime.utcfromtimestamp(int(m.timestamp[:-3])).
                replace(tzinfo=pytz.UTC),
            }
            for m in msgs
        ]
        return msgs

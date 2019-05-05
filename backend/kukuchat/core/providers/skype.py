from pathlib import Path
import tempfile
from datetime import datetime

from channels.auth import get_user
from threading import Thread

import skpy

from asgiref.sync import sync_to_async, async_to_sync

from core.providers.provider import BaseProvider
from core import utils


class SkypeProvider(BaseProvider):

    name = 'skype'

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'},
    }

    def __init__(self, scope, on_message_consumer):
        self.sk = skpy.Skype(connect=False)
        self.scope = scope
        self.on_message_consumer = on_message_consumer

    async def get_required_credentials(self, data):
        return self._required_credentials

    async def login(self, data):
        username = data['username']
        password = data['password']

        user_self = await get_user(self.scope)
        temp = tempfile.gettempdir() / Path(user_self.temp_dir)
        self._token_path = str(temp / 'token-skype-app')
        self.sk.conn.setTokenFile(self._token_path)

        try:
            self.sk.conn.readToken()
        except SkypeAuthException:
            self.sk.conn.setUserPwd(username, password)
            self.sk.conn.getSkypeToken()
            self.sk.conn.writeToken()
        self._start_listening()
        return {'msg': 'Successfully logged into Skype'}

    async def am_i_logged(self, data):
        is_logged = self.sk.conn.connected is True
        return {'is_logged': is_logged}

    async def get_chats(self, data):
        all_contacts = self.sk.contacts
        active_contacts = [c for c in all_contacts if c.id]
        chats = await utils.turn_provider_contacts_into_chats(
            active_contacts,
            lambda c: c.id,
            lambda c: f'{c.name.first} {c.name.last}',
            'skype'
        )
        return {'chats': [{'id': c.id, 'name': c.name} for c in chats]}

    async def post_login_action(self, data):
        pass

    async def send_message(self, uid, content):
        ch = self.sk.contacts[uid].chat
        ch.sendMsg(content)
        return {'provider': 'skype'}

    async def get_last_messages(self, uid, count):
        msgs = self.sk.chats[uid].getMsg()
        msgs = [{
            'provider': 'skype',
            'content': m.text,
            'me': m.author == self.skpy.contacts.userId,
            'time': datetime.utcfromtimestamp(int(m.timestamp[:-3])).
                replace(tzinfo=pytz.UTC)
                }
                for m in msgs]
        return msgs

    def _on_event(self, event):
        user = self.sk.contacts[event.msg.userId]
        name = f'{user.name.first} {user.name.last}'
        t = Thread(
            target=async_to_sync(self.on_message_consumer),
            kwargs={
                'provider': 'skype',
                'author_uid': event.msg.userId,
                'content': event.msg.content,
                'author_name': name,
            }
        )
        t.start()        

    def _start_listening(self):
        loop = skpy.SkypeEventLoop(tokenFile=self._token_path, autoAck=True)
        loop.onEvent = self._on_event
        loop.loop()

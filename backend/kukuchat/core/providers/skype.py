from pathlib import Path
import tempfile
from datetime import datetime

from channels.auth import get_user
from threading import Thread

import skpy
import pytz
from skpy import SkypeAuthException
from skpy import SkypeNewMessageEvent

from asgiref.sync import async_to_sync

from core.providers.provider import BaseProvider
from core import utils
from core import models


class SkypeProvider(BaseProvider):

    name = 'skype'

    _required_credentials = {
        'username': {'type': 'text', 'help': 'Nickname or phone number'},
        'password': {'type': 'password', 'help': 'Password'},
    }

    def __init__(self, scope, on_message_consumer):
        self.sk = skpy.Skype(connect=False)
        self.scope = scope
        self.user = None
        self.on_message_consumer = on_message_consumer

    async def get_required_credentials(self, data):
        return self._required_credentials

    async def login(self, data):
        username = data['username']
        password = data['password']

        self.user = await get_user(self.scope)

        temp = tempfile.gettempdir() / Path(self.user.temp_dir)
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

    async def _get_active_contacts(self):
        return models.Contacts(
            contacts=[c for c in self.sk.contacts if c.id],
            id_fun=lambda c: c.id,
            name_fun=lambda c: f'{c.name.first} {c.name.last}',
        )

    async def post_login_action(self, data):
        pass

    async def send_message(self, uid, content):
        ch = self.sk.contacts[uid].chat
        ch.sendMsg(content)
        return {'provider': 'skype'}

    async def get_last_messages(self, uid, count):
        try:
            msgs = self.sk.contacts[uid].chat.getMsgs()[:count]
            print(f'Got {len(msgs)} from {uid}. {msgs}')
        except Exception as e:
            print(str(e))
            print(f'Could not get messages from {uid}')
        msgs = [{
            'provider': 'skype',
            'content': m.content,
            'me': m.userId == self.sk.user.id,
            'time': datetime.utcfromtimestamp(int(m.timestamp[:-3])).
                replace(tzinfo=pytz.UTC)
                }
                for m in msgs]
        return msgs

    def _on_event(self, event):
        if not isinstance(event, SkypeNewMessageEvent):
            return
        user = self.sk.contacts[event.msg.userId]
        name = f'{user.name.first} {user.name.last}'
        t = Thread(
            target=async_to_sync(self.on_message_consumer),
            kwargs={
                'provider': 'skype',
                'author_uid': event.msg.userId,
                'content': event.msg.content,
                'author_name': name,
                'user': self.user,
            }
        )
        t.start()

    def _start_listening(self):
        loop = skpy.SkypeEventLoop(tokenFile=self._token_path, autoAck=True)
        loop.onEvent = self._on_event
        t = Thread(target=loop.loop)
        t.start()

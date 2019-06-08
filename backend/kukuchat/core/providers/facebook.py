from datetime import datetime
import json
import pathlib
import pytz
import tempfile

import fbchat
from fbchat.models import Message, ThreadType

from channels.auth import get_user

from core.providers.provider import BaseProvider
from core import models


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
        self.user = None

    def _get_cookies(self, path: pathlib.Path):
        if not path.exists():
            return None
        with open(path) as f:
            return json.load(f)

    def _save_cookies(self, path: pathlib.Path):
        with open(path, 'w') as f:
            json.dump(self.client.getSession(), f)

    async def get_required_credentials(self, data):
        return self._required_credentials

    async def logout(self):
        await self.client.logout()

    async def login(self, data):
        username = data['username']
        password = data['password']

        self.user = await get_user(self.scope)

        cookie_path = pathlib.Path(tempfile.gettempdir()) /\
            self.user.temp_dir / 'facebook_session.json'

        cookies = self._get_cookies(cookie_path)

        self.client = fbchat.Client()
        await self.client.start(username, password, session_cookies=cookies)

        self._save_cookies(cookie_path)

        self.client.onMessage = self._on_message
        self.client.listen(markAlive=True)

        return {'msg': 'Successfuly logged into Facebook'}

    async def am_i_logged(self, data):
        is_logged = self.client is not None and await self.client.isLoggedIn()
        return {'is_logged': is_logged}

    async def post_login_action(self, data):
        pass

    async def _get_active_contacts(self):
        all_contacts = await self.client.fetchAllUsers()
        return models.Contacts(
            contacts=[c for c in all_contacts if c.uid],
            id_fun=lambda c: c.uid,
            name_fun=lambda c: c.name,
        )

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
            user=self.user,
        )

    async def send_message(self, uid, content):
        await self.client.send(Message(text=content), uid)
        return {'provider': 'facebook'}

    async def get_last_messages(self, uid, count):
        try:
            msgs = await self.client.fetchThreadMessages(uid, limit=count)
        except Exception as e:
            print(str(e))
            return []
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

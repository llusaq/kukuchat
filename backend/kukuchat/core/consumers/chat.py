import pathlib
import tempfile

from django.contrib.auth import authenticate

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import login, get_user, logout
from channels.db import database_sync_to_async

from asgiref.sync import async_to_sync

from core.providers import facebook
from core.providers import skype
from core.providers import telegram
from core import utils
from core import models


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()

        self.facebook = facebook.FacebookProvider(self.scope, self.on_message_consumer)
        self.skype = skype.SkypeProvider(self.scope, self.on_message_consumer)
        self.telegram = telegram.TelegramProvider(self.scope)

    async def disconnect(self, code):
        pass

    def on_message_consumer(self, provider, author_uid, author_name, content):
        chat = utils.get_chat_for_provider_contact(provider, author_uid, author_name)
        async_to_sync(self.send_json)({
            'action': 'new_message',
            'chat_id': chat.id,
            'content': content,
        })

    async def receive_json(self, data):
        user = await get_user(self.scope)
        try:
            action = data['action']

            if not user.is_authenticated and action not in ['login', 'am_i_logged']:
                raise Exception('Please log in first')
            if action.startswith('provider'):
                _, provider_name, method_name = action.split('_', 2)
                provider_instance = getattr(self, provider_name)
                method = getattr(provider_instance, method_name)
                resp = await method(data)
                if method_name == 'login':
                    await utils.store_creds(user, provider_instance, data)
            else:
                method = getattr(self, action)
                resp = await method(data)
        except Exception as e:
            await self.send_json({
                'action': action,
                'status': 'error',
                'msg': str(e),
            })
        else:
            await self.send_json({'status': 'ok', 'action': action, **resp})

    async def login(self, data):
        user = await database_sync_to_async(authenticate)(
            username=data['username'],
            password=data['password'],
        )
        if not user:
            return {'status': 'error', 'msg': 'Bad credentials'}

        await login(self.scope, user)
        await database_sync_to_async(self.scope['session'].save)()
        await self._create_dir(user)

        await utils.autolog(
            user,
            [
                ('facebook', self.facebook),
                ('skype', self.skype),
                ('telegram', self.telegram),
            ]
        )

        return {'msg': 'Logged in successfully'}

    async def am_i_logged(self, data):
        user = await get_user(self.scope)
        resp = {'is_logged': user.is_authenticated, 'username': user.username}
        return resp

    async def logout(self, data):
        await logout(self.scope)
        return {'msg': 'Logged out successfuly'}

    async def _create_dir(self, user):
        temp = tempfile.gettempdir()
        path = pathlib.Path(temp) / user.temp_dir
        path.mkdir(parents=True, exist_ok=True)

    async def send_message(self, data):
        chat = await database_sync_to_async(models.Chat.objects.get)(pk=data['chat_id'])
        contact = await database_sync_to_async(chat.contact_set.get)(provider=data['provider'])
        provider_inst = getattr(self, data['provider'])
        result = await provider_inst.send_message(uid=contact.uid, content=data['content'])
        return {'chat_id': chat.id, 'content': data['content'], **result}

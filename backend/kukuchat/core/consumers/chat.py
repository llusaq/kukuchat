import pathlib
import tempfile

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import login, get_user, logout
from channels.db import database_sync_to_async

from asgiref.sync import async_to_sync

from core.providers import facebook
from core.providers import skype
from core import utils


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()

        user = await get_user(self.scope)

        self.facebook = facebook.FacebookProvider(self.scope)
        self.skype = skype.SkypeProvider(self.scope)

        if not isinstance(user, AnonymousUser):
            await utils.autolog(
                user,
                [
                    ('facebook', self.facebook),
                    ('skype', self.skype),
                ]
            )

    async def disconnect(self, code):
        pass

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
        user = await database_sync_to_async(lambda: get_user_model().objects.get(
            username=data['username']
        ))()
        if not user:
            return {'status': 'error', 'msg': 'Bad credentials'}
        await login(self.scope, user)
        await database_sync_to_async(self.scope['session'].save)()
        await self._create_dir(user)
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



from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import login, get_user
from channels.db import database_sync_to_async

from asgiref.sync import sync_to_async


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive_json(self, data):
        try:
            action = data['action']
            method = getattr(self, action)
            resp = await method(data)
        except Exception as e:
            await self.send_json({
                'status': 'error',
                'msg': str(e),
            })
        else:
            await self.send_json(resp)

    async def login(self, data):
        user = await database_sync_to_async(lambda: get_user_model().objects.get(
            username=data['username']
        ))()
        if not user:
            return {'status': 'error', 'msg': 'Bad credentials'}
        await login(self.scope, user)
        await database_sync_to_async(self.scope['session'].save)()
        return {'status': 'ok', 'msg': 'Logged in successfully'}

    async def am_i_logged(self, data):
        is_logged = bool(get_user(self.scope))
        await self.send_json({'status': 'ok', 'is_logged': is_logged})

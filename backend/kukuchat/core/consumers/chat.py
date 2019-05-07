from collections.abc import Sequence
from datetime import datetime as dt
import itertools
import pathlib
import pytz
import tempfile

from django.contrib.auth import authenticate
from django.db.models import Case, When

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import login, get_user, logout
from channels.db import database_sync_to_async

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

    async def merge_chats(self, data):
        ids = data['chat_ids']
        to_delete = ids[1:]
        order = Case(*[When(id=pk, then=i) for i, pk in enumerate(ids)])
        user = await get_user(self.scope)
        chats = models.Chat.objects.filter(id__in=ids).order_by(order)
        for c in chats:
            for owner in (con.owner for con in c.contact_set.all()):
                if not owner == user:
                    raise Exception('You dont own some of contacts')
        first, *rest = chats
        for c in chats:
            for con in c.contact_set.all():
                con.chat = first
                await database_sync_to_async(con.save)()
        models.Chat.objects.filter(pk__in=to_delete).delete()
        return {'from_ids': ids, 'chat_id': first.id, 'chat_name': first.name}

    async def on_message_consumer(self, provider, author_uid, author_name, content, time=None):
        if not time:
            time = dt.utcnow().replace(tzinfo=pytz.UTC)
        chat = await utils.get_chat_for_provider_contact(provider, author_uid, author_name, await get_user(self.scope))
        await self.send_json({
            'action': 'new_message',
            'chat_id': chat.id,
            'provider': provider,
            'content': content,
            'time': str(time),
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
            return await self.send_json({
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

    async def get_messages(self, data):
        chats = await database_sync_to_async(models.Chat.objects.filter)(
            pk__in=data['chat_ids'],
        )
        chats = await database_sync_to_async(chats.prefetch_related)('contact_set')
        ret = {}
        for contact in itertools.chain(*[c.contact_set.all() for c in chats]):
            provider = getattr(self, contact.provider)
            messages = ret.setdefault(contact.chat.id, [])
            msgs = await provider.get_last_messages(
                uid=contact.uid,
                count=data.get('count', 20)
            )
            messages.extend(msgs)
        return {
            'chats': [
                {
                    'id': c_id,
                    'messages': [
                        {
                            'content': m['content'],
                            'provider': m['provider'],
                            'me': m['me'],
                            'time': str(m['time']),
                        }
                        for m in msgs
                    ]
                }
                for c_id, msgs in ret.items()
            ]
        }

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
        print(contact.uid)
        result = await provider_inst.send_message(uid=contact.uid, content=data['content'])
        return {'chat_id': chat.id, 'content': data['content'], **result}

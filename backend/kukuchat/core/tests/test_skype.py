import asyncio
from datetime import datetime as dt
from unittest.mock import MagicMock
import tempfile
import os
from types import SimpleNamespace


from django.core import signing

from channels.auth import get_user

import pytest
import skpy

from core.tests.fixtures import *
from core.models import Chat, Contact


class MessageEvent(skpy.event.SkypeNewMessageEvent):
    def __init__(self):
        self.__dict__['msg'] = SimpleNamespace(
            content='Priviet maniunia',
            userId='123',
            time=dt(2019, 5, 4, 10),
        )

    def __getattr__(self, name):
        return self.__dict__['msg']

    def __str__(self):
        return ''

    def __repr__(self):
        return ''


class SkypeContactsMock:
    def getMsgs(self):
        return [
            SimpleNamespace(
                content='whats up',
                userId='123',
                timestamp='1556834306289',
            ),
            SimpleNamespace(
                content='I am fine',
                userId='me',
                timestamp='1556834206289',
            ),
        ]

    contacts = [
        SimpleNamespace(
            id='123',
            name=SimpleNamespace(
                first='Tomasz',
                last='jD',
            ),
        )
    ]

    def __iter__(self):
        self.it = iter(self.contacts)
        return self.it

    def __next__(self):
        return next(self.it)

    def __getitem__(self, idx):
        for c in self.contacts:
            if c.id == idx:
                c.getMsgs = self.getMsgs
                return c


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
def my_skype_chat(monkeypatch):
    monkeypatch.setattr(skpy, 'Skype', MagicMock())
    monkeypatch.setattr(skpy, 'SkypeEventLoop', MagicMock())


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_log_to(comm):
    await comm.send_json_to({
        'action': 'provider_skype_am_i_logged',
    })

    resp = await comm.receive_json_from()

    assert resp == {'status': 'ok', 'action': 'provider_skype_am_i_logged', 'is_logged': False}

    await comm.send_json_to({
        'action': 'provider_skype_login',
        'username': '579631148',
        'password': '12qwertyU',
    })
    f = asyncio.Future()
    f.set_result(None)

    resp = await comm.receive_json_from()

    tmpdir = tempfile.gettempdir()
    dirname = (await get_user(comm.instance.scope)).temp_dir

    skpy.Skype.return_value.conn.setTokenFile.assert_called_once_with(
        os.path.join(tmpdir, dirname, 'token-skype-app')
    )
    skpy.Skype.return_value.conn.readToken.assert_called_once_with()
    skpy.Skype.return_value.conn.setUserPwd.assert_not_called()
    skpy.Skype.return_value.conn.getSkypeToken.assert_not_called()
    skpy.Skype.return_value.conn.connected = True

    assert resp == {
        'action': 'provider_skype_login',
        'status': 'ok',
        'msg': 'Successfully logged into Skype',
    }
    await comm.send_json_to({
        'action': 'provider_skype_am_i_logged',
    })

    resp = await comm.receive_json_from()

    assert resp == {'status': 'ok', 'action': 'provider_skype_am_i_logged', 'is_logged': True}
    await comm.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_required_cred(comm):
    await comm.send_json_to({
        'action': 'provider_skype_get_required_credentials',
    })

    resp = await comm.receive_json_from()

    assert resp == {
        'status': 'ok',
        'action': 'provider_skype_get_required_credentials',
        'username': {'type': 'text', 'help': 'Nickname or phone number'},
        'password': {'type': 'password', 'help': 'Password'}
    }
    await comm.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_list_chats(logged_skype):
    await logged_skype.send_json_to({
        'action': 'get_chats',
    })
    f = [
        SimpleNamespace(
            name=SimpleNamespace(
                first='Andrzej',
                last='Pączek',
            ),
            id=1,
        ),
        SimpleNamespace(
            name=SimpleNamespace(
                first='Piotr',
                last='Czaja',
            ),
            id=3,
        ),
    ]

    skpy.Skype.return_value.contacts = f
    resp = await logged_skype.receive_json_from()
    chats = resp['chats']

    assert Chat.objects.all().count() == len(chats)
    assert 'Andrzej Pączek' in [c['name'] for c in resp['chats']]
    await logged_skype.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_store_creds(comm):
    await comm.send_json_to({
        'action': 'provider_skype_login',
        'username': '579631148',
        'password': '12qwertyU',
    })

    await comm.receive_json_from()

    user = await get_user(comm.instance.scope)

    creds = signing.loads(user.credentials)

    assert creds['skype'] == {'username': '579631148', 'password': '12qwertyU'}

    await comm.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_send_messages(logged_skype):

    andrzej_uid = 'andriy5852'
    andrzej = await database_sync_to_async(Contact.objects.create)(
        provider='skype',
        uid=andrzej_uid,
        chat=await database_sync_to_async(Chat.objects.create)(name='Andrzej'),
        owner=await get_user(logged_skype.instance.scope),
    )
    await logged_skype.send_json_to({
        'action': 'send_message',
        'provider': 'skype',
        'chat_id': andrzej.chat.id,
        'content': 'Priviet maniunia'
    })
    f = asyncio.Future()
    f.set_result(None)
    contact_mock = MagicMock()
    skpy.Skype.return_value.contacts.__getitem__.return_value = contact_mock
    send_mock = contact_mock.chat.sendMsg
    send_mock.return_value = f

    resp = await logged_skype.receive_json_from()
    skpy.Skype.return_value.contacts.__getitem__.assert_called_once_with(andrzej_uid)
    send_mock.assert_called_once_with('Priviet maniunia')
    assert send_mock.call_args[0][0] == 'Priviet maniunia'

    assert resp == {
        'action': 'send_message',
        'chat_id': andrzej.chat.id,
        'provider': 'skype',
        'status': 'ok',
        'content': 'Priviet maniunia'
    }
    await logged_skype.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_receive_messages(logged_skype):
    skpy.Skype.return_value.contacts = SkypeContactsMock()

    skpy.SkypeEventLoop.return_value.onEvent(
        MessageEvent(),
    )

    resp = await logged_skype.receive_json_from()

    chat = Contact.objects.get(chat__name='Tomasz jD')
    resp == {
        'action': 'new_message',
        'content': 'Priviet maniunia',
        'userId': chat.id,
        'provider': 'skype',
    }

    assert resp['content'] == 'Priviet maniunia'
    assert resp['chat_id'] == chat.id

    await logged_skype.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_get_chat_messages(logged_skype):
    skpy.Skype.return_value.chats = SkypeContactsMock()
    chat = Chat.objects.create(name='Tomasz Dul')
    Contact.objects.create(
        provider='skype',
        uid='123',
        chat=chat,
        owner=await get_user(logged_skype.instance.scope),

    )

    f = asyncio.Future()
    f.set_result([])

    skpy.Skype.return_value.getMsgs.return_value = f
    skpy.Skype.return_value.user.id = 'me'

    await logged_skype.send_json_to({
        'action': 'get_messages',
        'chat_ids': [chat.id],
        'count': 50,
    })

    resp = await logged_skype.receive_json_from()

    assert resp == {
        'action': 'get_messages',
        'chats': [{
            'id': chat.id,
            'messages': [
                {
                    'provider': 'skype',
                    'content': 'whats up',
                    'me': False,
                    'time': '2019-05-02 21:58:26+00:00',
                },
                {
                    'provider': 'skype',
                    'content': 'I am fine',
                    'me': True,
                    'time': '2019-05-02 21:56:46+00:00',
                },
            ],
        }],
        'status': 'ok',
    }

    await logged_skype.disconnect()

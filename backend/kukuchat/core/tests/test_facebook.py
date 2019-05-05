import asyncio
from types import SimpleNamespace
from unittest.mock import MagicMock

from channels.db import database_sync_to_async
from channels.auth import get_user

from fbchat import ThreadType
import pytest

from core.tests.fixtures import *
from core.models import Chat, Contact

import fbchat


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
def my_fb_chat(monkeypatch):
    monkeypatch.setattr(fbchat, 'Client', MagicMock())


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_log_in(comm):
    await comm.send_json_to({
        'action': 'provider_facebook_am_i_logged',
    })

    resp = await comm.receive_json_from()

    assert resp == {'status': 'ok', 'action': 'provider_facebook_am_i_logged', 'is_logged': False}

    await comm.send_json_to({
        'action': 'provider_facebook_login',
        'username': '579631148',
        'password': '12qwertyU',
    })

    f = asyncio.Future()
    f.set_result(True)
    fbchat.Client.return_value.isLoggedIn.return_value = f

    start_mock = fbchat.Client.return_value.start

    f = asyncio.Future()
    f.set_result(None)
    start_mock.return_value = f

    resp = await comm.receive_json_from()

    start_mock.assert_called_once_with('579631148', '12qwertyU')

    assert resp == {
        'action': 'provider_facebook_login',
        'status': 'ok',
        'msg': 'Successfuly logged into Facebook'
    }

    await comm.send_json_to({
        'action': 'provider_facebook_am_i_logged',
    })

    resp = await comm.receive_json_from()

    assert resp == {'status': 'ok', 'action': 'provider_facebook_am_i_logged', 'is_logged': True}
    await comm.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_required_creds(comm):
    await comm.send_json_to({
        'action': 'provider_facebook_get_required_credentials',
    })

    resp = await comm.receive_json_from()

    assert resp == {
        'status': 'ok',
        'action': 'provider_facebook_get_required_credentials',
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'}
    }

    await comm.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_list_chats(logged_fb):
    await logged_fb.send_json_to({
        'action': 'provider_facebook_get_chats',
    })

    f = asyncio.Future()
    f.set_result([
        SimpleNamespace(
            name='Maciej Fraszczak',
            uid=1,
        ),
        SimpleNamespace(
            name='Tomasz Dul',
            uid=2,
        ),
    ])

    fbchat.Client.return_value.fetchAllUsers.return_value = f

    resp = await logged_fb.receive_json_from()
    chats = resp['chats']

    assert Chat.objects.all().count() == len(chats)

    assert 'Maciej Fraszczak' in (c['name'] for c in resp['chats'])
    await logged_fb.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_send_messages(logged_fb):

    dariusz_uid = '100035479385797'
    dariusz = await database_sync_to_async(Contact.objects.create)(
        provider='facebook',
        uid=dariusz_uid,
        chat=await database_sync_to_async(Chat.objects.create)(name='Dariusz'),
        owner=await get_user(logged_fb.instance.scope),
    )

    await logged_fb.send_json_to({
        'action': 'send_message',
        'provider': 'facebook',
        'chat_id': dariusz.chat.id,
        'content': 'Hi man',
    })

    f = asyncio.Future()
    f.set_result(None)
    send_mock = fbchat.Client.return_value.send
    send_mock.return_value = f

    resp = await logged_fb.receive_json_from()

    send_mock.assert_called_once()
    assert send_mock.call_args[0][0].text == 'Hi man'
    assert send_mock.call_args[0][1] == dariusz_uid

    assert resp == {
        'action': 'send_message',
        'chat_id': dariusz.chat.id,
        'provider': 'facebook',
        'status': 'ok',
        'content': 'Hi man',
    }

    await logged_fb.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_receive_messages(logged_fb):
    f = asyncio.Future()
    f.set_result({'123': SimpleNamespace(name='Andrii Donets')})
    fbchat.Client.return_value.fetchUserInfo.return_value = f

    await fbchat.Client.return_value.onMessage(
        message_object=SimpleNamespace(
            text='hey man',
            timestamp='1556834306289',
        ),
        author_id='123',
        thread_type=ThreadType.USER,
    )

    resp = await logged_fb.receive_json_from()

    chat = Contact.objects.get(chat__name='Andrii Donets')

    resp == {
        'action': 'new_message',
        'content': 'hey man',
        'chat_id': chat.id,
        'provider': 'facebook',
    }
    assert resp['content'] == 'hey man'
    assert resp['chat_id'] == chat.id

    await logged_fb.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_get_chat_messages(logged_fb):
    chat = Chat.objects.create(name='Tomasz Dul')
    Contact.objects.create(
        provider='facebook',
        uid='123',
        chat=chat,
        owner=await get_user(logged_fb.instance.scope),
    )

    f = asyncio.Future()
    f.set_result([
        SimpleNamespace(
            text='hey man',
            author='123',
            timestamp='1556834306289',
        ),
        SimpleNamespace(
            text='whats up?',
            author='me',
            timestamp='1556834206289'
        ),
    ])
    fbchat.Client.return_value.fetchThreadMessages.return_value = f
    fbchat.Client.return_value.uid = 'me'

    await logged_fb.send_json_to({
        'action': 'get_messages',
        'chat_id': chat.id,
        'count': 50,
    })

    resp = await logged_fb.receive_json_from()

    assert resp == {
        'action': 'get_messages',
        'chat_id': chat.id,
        'messages': [
            {
                'provider': 'facebook',
                'content': 'hey man',
                'me': False,
                'time': '2019-05-02 21:58:26+00:00',
            },
            {
                'provider': 'facebook',
                'content': 'whats up?',
                'me': True,
                'time': '2019-05-02 21:56:46+00:00',
            },
        ],
        'status': 'ok',
    }

    await logged_fb.disconnect()

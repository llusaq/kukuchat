import pytest

from channels.db import database_sync_to_async

from core.tests.fixtures import *
from core.models import Chat, Contact


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

    resp = await comm.receive_json_from()

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
async def test_store_creds(logged_fb):
    await logged_fb.send_json_to({
        'action': 'provider_facebook_get_chats',
    })

    resp = await logged_fb.receive_json_from()
    chats = resp['chats']

    assert Chat.objects.all().count() == len(chats)

    assert 'Maciej Fraszczak' in (c['name'] for c in resp['chats'])
    await logged_fb.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_send_and_receive_messages(logged_fb_mj, logged_fb_da):

    dariusz_uid = '100035479385797'
    dariusz = await database_sync_to_async(Contact.objects.create)(
        provider='facebook',
        uid=dariusz_uid,
        name='Dariusz',
        chat=await database_sync_to_async(Chat.objects.create)(name='Chat with Dariusz')
    )

    await logged_fb_mj.send_json_to({
        'action': 'send_message',
        'provider': 'facebook',
        'chat_id': dariusz.chat.id,
        'content': 'Hi man',
    })

    resp = await logged_fb_mj.receive_json_from()

    assert resp == {
        'action': 'send_message',
        'chat_id': dariusz.chat.id,
        'provider': 'facebook',
        'status': 'ok',
        'content': 'Hi man',
    }

    resp = await logged_fb_da.receive_json_from()

    assert resp == {
        'action': 'event_new_message',
        'chat_id': dariusz.chat.id,
        'provider': 'facebook',
        'content': 'Hi man',
    }

    await logged_fb_mj.disconnect()
    await logged_fb_da.disconnect()

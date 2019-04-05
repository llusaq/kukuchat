import pytest

from django.core import signing

from channels.auth import get_user

from core.tests.fixtures import *
from core.models import Chat


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
async def test_store_creds(logged):
    await logged.send_json_to({
        'action': 'provider_facebook_get_chats',
    })

    resp = await logged.receive_json_from()
    chats = resp['chats']

    assert Chat.objects.all().count() == len(chats)

    assert 'Maciej Fraszczak' in (c['name'] for c in resp['chats'])
    await logged.disconnect()

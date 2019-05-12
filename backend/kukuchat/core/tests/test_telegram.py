import asyncio
from types import SimpleNamespace
from unittest.mock import MagicMock

from channels.db import database_sync_to_async
from channels.auth import get_user

from fbchat import ThreadType
import pytest

from core.tests.fixtures import *
from core.models import Chat, Contact


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_log_in(comm):
    await comm.send_json_to({
        'action': 'provider_telegram_am_i_logged',
    })

    resp = await comm.receive_json_from()

    assert resp == {
        'status': 'ok',
        'action': 'provider_telegram_am_i_logged',
        'is_logged': False
        }

    await comm.send_json_to({
        'action': 'provider_telegram_login',
        'username': 'test1',
    })

    resp = await comm.receive_json_from()

    assert resp == {
        'action': 'provider_telegram_login',
        'status': 'ok',
        'msg': 'Succesfully logged into Telegram'
    }

    await comm.send_json_to({
        'action': 'provider_telegram_am_i_logged',
    })

    resp = await comm.receive_json_from()

    assert resp == {
        'status': 'ok',
        'action': 'provider_telegram_am_i_logged',
        'is_logged': True
    }

    await comm.disconnect()

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_required_creds(comm):
    await comm.send_json_to({
        'action': 'provider_telegram_get_required_credentials',
    })

    resp = await comm.receive_json_from()

    assert resp == {
        'status': 'ok',
        'action': 'provider_telegram_get_required_credentials',
        'username': {'type': 'text', 'help': 'Unique username or phone number'},
    }

    await comm.disconnect()

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_list_chats(comm):
    await comm.send_json_to({
        'action': 'provider_telegram_get_chats',
    })

    resp = await comm.receive_json_from()
    print(resp)

    chats = resp['chats']

    assert Chat.objects.all().count() == len(chats)

    assert 'medford' in (c['first_name'] for c in resp['chats'])
    await comm.disconnect()
    
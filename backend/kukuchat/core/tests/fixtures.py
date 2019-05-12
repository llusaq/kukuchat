import asyncio
from unittest.mock import MagicMock
import string
import random

from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator

import pytest
import fbchat
import skpy

from kukuchat.routing import application


@pytest.fixture
@pytest.mark.asyncio
async def comm(db, client):
    password = ''.join(random.choices(string.ascii_letters, k=8))
    username = ''.join(random.choices(string.ascii_letters, k=8))

    await database_sync_to_async(get_user_model().objects.create_user)(
        username=username,
        password=password,
        email='test@test.com',
    )

    comm = WebsocketCommunicator(application, 'ws/chat/')

    await comm.connect()

    await comm.send_json_to({
        'action': 'login',
        'username': username,
        'password': password,
    })

    await comm.receive_json_from()

    return comm


@pytest.fixture
@pytest.mark.asyncio
async def logged_fb(db, client, monkeypatch):
    password = ''.join(random.choices(string.ascii_letters, k=8))
    username = ''.join(random.choices(string.ascii_letters, k=8))

    await database_sync_to_async(get_user_model().objects.create_user)(
        username=username,
        password=password,
        email='test@test.com',
    )

    comm = WebsocketCommunicator(application, 'ws/chat/')

    await comm.connect()

    await comm.send_json_to({
        'action': 'login',
        'username': username,
        'password': password,
    })

    await comm.receive_json_from()

    monkeypatch.setattr(fbchat, 'Client', MagicMock())

    f = asyncio.Future()
    f.set_result(None)

    fbchat.Client.return_value.start.return_value = f

    await comm.send_json_to({
        'action': 'provider_facebook_login',
        'username': '579631148',
        'password': '12qwertyU',
    })

    await comm.receive_json_from()

    return comm

@pytest.fixture
@pytest.mark.asyncio
async def logged_skype(db, client, monkeypatch):
    password = ''.join(random.choices(string.ascii_letters, k=8))
    username = ''.join(random.choices(string.ascii_letters, k=8))

    await database_sync_to_async(get_user_model().objects.create_user)(
        username=username,
        password=password,
        email='test@test.com',
    )

    comm = WebsocketCommunicator(application, 'ws/chat/')

    await comm.connect()

    await comm.send_json_to({
        'action': 'login',
        'username': username,
        'password': password,
    })

    await comm.receive_json_from()

    await comm.send_json_to({
        'action': 'provider_skype_login',
        'username': '579631148',
        'password': '12qwertyU',
    })

    await comm.receive_json_from()

    return comm

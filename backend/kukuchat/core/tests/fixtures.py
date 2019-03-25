import string
import random
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator

import pytest

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

from django.contrib.auth import get_user_model

from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

import pytest

from core.consumers.chat import ChatConsumer
from kukuchat.routing import application


@pytest.mark.django_db
def test_user_register(client):
    user = client.post('/api/register/',{'username': 'user1','password': '12qwertyU','email': 'user1@yopmail.com'})
    assert get_user_model().objects.all().count() == 1
    results = get_user_model().objects.all().values('username', 'email')
    results = list(results)
    assert results == [{'username': 'user1', 'email': 'user1@yopmail.com'}]


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_user_can_login():
    user = await database_sync_to_async(lambda: get_user_model().objects.create_user(
        username='test',
        password='test',
        email='test@test.test',
    ))()

    data = {
        'action': 'login',
        'username': user.username,
        'password': 'test',
    }

    communicator = WebsocketCommunicator(application, 'ws/chat/')

    connected, subprotocol = await communicator.connect()
    assert connected

    await communicator.send_json_to(data)

    resp = await communicator.receive_json_from()

    assert resp == {'status': 'ok', 'msg': 'Logged in successfully'}

    await communicator.disconnect()

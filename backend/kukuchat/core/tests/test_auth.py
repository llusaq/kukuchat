from django.contrib.auth import get_user_model

from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

import pytest

from core.consumers.chat import ChatConsumer
from kukuchat.routing import application


@pytest.mark.django_db(transaction=True)
def test_user_register(client):
    user = client.post('/api/register/',{'username': 'user1','password': '12qwertyU','email': 'user1@yopmail.com'})
    assert get_user_model().objects.all().count() == 1
    results = get_user_model().objects.all().values('username', 'email')
    results = list(results)
    assert results == [{'username': 'user1', 'email': 'user1@yopmail.com'}]


@pytest.mark.django_db(transaction=True)
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

    assert resp == {'action': 'login', 'status': 'ok', 'msg': 'Logged in successfully'}

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_user_can_check_login_state():
    data = {
        'action': 'am_i_logged',
    }

    await database_sync_to_async(lambda: get_user_model().objects.create_user(
        username='test1',
        password='test1',
        email='test1@test.test',
    ))()

    communicator = WebsocketCommunicator(application, 'ws/chat/')

    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to(
        {
            'action': 'login',
            'username': 'test1',
            'password': 'test1',
        }
    )

    await communicator.send_json_to(data)

    await communicator.receive_json_from()

    resp = await communicator.receive_json_from()

    assert resp == {'action': 'am_i_logged', 'status': 'ok', 'is_logged': True, 'username': 'test1'}

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_user_can_logout():
    await database_sync_to_async(get_user_model().objects.create_user)(
        username='test',
        password='test',
        email='test@test.com',
    )

    communicator = WebsocketCommunicator(application, 'ws/chat/')

    await communicator.connect()
    await communicator.send_json_to({
        'action': 'login',
        'username': 'test',
        'password': 'test',
    })

    resp = await communicator.receive_json_from()

    await communicator.send_json_to({
        'action': 'am_i_logged',
    })

    resp = await communicator.receive_json_from()

    assert resp['is_logged'] is True

    await communicator.send_json_to({
        'action': 'logout',
    })

    resp = await communicator.receive_json_from()

    assert resp == {'status': 'ok', 'action': 'logout', 'msg': 'Logged out successfuly'}

    await communicator.send_json_to({
        'action': 'am_i_logged',
    })

    resp = await communicator.receive_json_from()

    assert resp['is_logged'] is False

    await communicator.disconnect()

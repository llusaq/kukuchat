import asyncio

import pytest

from core.tests.fixtures import *
from core.consumers.chat import ChatConsumer


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_schedule_get_messages(comm, monkeypatch):
    monkeypatch.setattr(ChatConsumer, 'get_messages', MagicMock())

    f = asyncio.Future()
    f.set_result({'foo': 'bar'})
    ChatConsumer.get_messages.return_value = f

    data = {
        'action': 'schedule',
        'provider': 'facebook',
        'method': 'get_messages',
        'chat_ids': [1, 2, 3],
    }
    await comm.send_json_to(data)
    resp = await comm.receive_json_from()
    resp = await comm.receive_json_from()
    assert resp == {'action': 'get_messages', 'foo': 'bar'}
    resp = await comm.receive_json_from()
    assert resp == {'action': 'get_messages', 'foo': 'bar'}
    resp = await comm.receive_json_from()
    assert resp == {'action': 'get_messages', 'foo': 'bar'}

    await comm.disconnect()

import asyncio

import pytest

from channels.auth import get_user

from core.tests.fixtures import *
from core.models import Contact, Chat
from core.scheduler import Scheduler


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_schedule_task(comm, monkeypatch):
    monkeypatch.setattr(Scheduler, 'add_task', MagicMock())
    monkeypatch.setattr(asyncio, 'create_task', MagicMock())

    data = {'action': 'schedule', 'method': 'make_foo'}
    await comm.send_json_to(data)
    resp = await comm.receive_json_from()
    assert resp == {**data, 'status': 'ok', 'scheduled': True}
    asyncio.create_task.assert_called_once_with(Scheduler.add_task.return_value)

    await comm.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_log_in(comm):
    chats = [
        Chat.objects.create(
            name='Andrii Donets',
        ),
        Chat.objects.create(
            name='Andrzej Pączek',
        ),
        Chat.objects.create(
            name='medf0rd',
        ),
        Chat.objects.create(
            name='unrelated',
        ),
    ]

    user = await get_user(comm.instance.scope)

    contacts = [
        Contact.objects.create(
            provider='facebook',
            uid='123',
            chat=chats[0],
            owner=user,
        ),
        Contact.objects.create(
            provider='other',
            uid='123',
            chat=chats[0],
            owner=user,
        ),
        Contact.objects.create(
            provider='skype',
            uid='234',
            chat=chats[1],
            owner=user,
        ),
        Contact.objects.create(
            provider='telegram',
            uid='452',
            chat=chats[2],
            owner=user,
        ),
        Contact.objects.create(
            provider='unrelated',
            uid='452',
            chat=chats[3],
            owner=user,
        ),
    ]

    await comm.send_json_to({
        'action': 'merge_chats',
        'chat_ids': [chats[1].id, chats[0].id, chats[2].id],
    })

    resp = await comm.receive_json_from()

    [c.refresh_from_db() for c in contacts]

    assert Contact.objects.all().count() == 5
    assert Chat.objects.all().count() == 2

    chat = Chat.objects.get(name='Andrzej Pączek')

    for c in contacts[:-1]:
        assert c.chat == chat

    assert contacts[-1].chat == Chat.objects.get(name='unrelated')

    assert resp == {
        'status': 'ok',
        'action': 'merge_chats',
        'from_ids': [chats[1].id, chats[0].id, chats[2].id],
        'chat_id': chat.id,
        'chat_name': chat.name,
    }

    await comm.disconnect()

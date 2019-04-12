import pytest

from django.core import signing

from channels.auth import get_user

from core.tests.fixtures import *


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


    
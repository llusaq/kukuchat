from uuid import uuid4
from pprint import pprint

from django.core import signing

from channels.auth import get_user

import pytest

from core.tests.fixtures import *


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_log_to(comm):
    await comm.send_json_to({
        'action': 'provider_skype_am_i_logged',
    })

    resp = await comm.receive_json_from()

    assert resp == {'status': 'ok', 'action': 'provider_skype_am_i_logged', 'is_logged':False}

    await comm.send_json_to({
        'action': 'provider_skype_login',
        'username': '579631148',
        'password': '12qwertyU',
    })

    resp = await comm.receive_json_from()

    assert resp == {
        'action': 'provider_skype_login',
        'status': 'ok',
        'msg': 'Successfully logged into Skype',
    }
    await comm.send_json_to({
        'action': 'provider_skype_am_i_logged',
    })

    resp = await comm.receive_json_from()

    assert resp == {'status': 'ok', 'action': 'provider_skype_am_i_logged', 'is_logged':True}
    await comm.disconnect()

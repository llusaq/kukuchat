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
    import ipdb ; ipdb.set_trace() 

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

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_required_cred(comm):
    await comm.send_json_to({
        'action': 'provider_skype_get_required_credentials',
    })

    resp = await comm.receive_json_from()

    assert resp == {
        'status': 'ok',
        'action': 'provider_skype_get_required_credentials',
        'username': {'type': 'text', 'help': 'Email or phone number'},
        'password': {'type': 'password', 'help': 'Password'}
    }
    await comm.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_store_creds(comm):
    await comm.send_json_to({
        'action': 'provider_skype_login',
        'username': '579631148',
        'password': '12qwertyU',
    })

    resp = await comm.receive_json_from()

    user = await get_user(comm.instance.scope)

    creds = signing.loads(user.credentials)

    assert creds['skype'] == {'username': '579631148', 'password': '12qwertyU'}

    await comm.disconnect()
    
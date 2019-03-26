import asyncio
from unittest.mock import patch, MagicMock

from django.core import signing

import pytest

from channels.auth import get_user

from core.tests.fixtures import *
from core import utils


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_autolog(comm):
    user = await get_user(comm.instance.scope)
    creds = {'facebook': {'username': 'test', 'password': 'fbpass'}}
    creds = signing.dumps(creds)
    user.credentials = creds
    user.save()
    with patch('core.providers.facebook.FacebookProvider', autospec=True) as fb_mock:
        async def login(): pass
        fb_mock.return_value.login.return_value = login()
        await utils.autolog(user, [('facebook', fb_mock.return_value)])
    fb_mock.return_value.login.assert_called_once_with({
        'username': 'test',
        'password': 'fbpass',
    })

    await comm.disconnect()

import pytest

from core.tests.fixtures import *


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_list_friends(comm):
    await comm.send_json_to({'action': 'am_i_logged'})
    resp = await comm.receive_json_from()
    await comm.disconnect()

    # TODO: Finish this

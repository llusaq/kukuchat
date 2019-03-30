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



































# class SkypeTests(TestCase): 

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.sk = Skype(connect=False)
#         cls.sk.conn
#         cls.sk.conn.setTokenFile(".token-skype-app")
#         try:
#             cls.sk.conn.readToken()
#         except SkypeAuthException:
#             cls.sk.conn.setUserPwd('579631148', '12qwertyU')
#             cls.sk.conn.getSkypeToken()

#     def test_send_msg(self):
#         id_message = str(uuid4())
#         ch = self.sk.contacts.contact("andriy5852").chat
#         ch.sendMsg(id_message)

#         results = ch.getMsgs()
#         self.assertEqual(id_message, results[0].content)
from unittest.mock import patch
from pprint import pprint
from skpy import Skype
from django.test import TestCase
from skpy import SkypeAuthException
from uuid import uuid4


class SkypeTests(TestCase): 

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sk = Skype(connect=False)
        cls.sk.conn
        cls.sk.conn.setTokenFile(".token-skype-app")
        try:
            cls.sk.conn.readToken()
        except SkypeAuthException:
            cls.sk.conn.setUserPwd('579631148', '12qwertyU')
            cls.sk.conn.getSkypeToken()

    def test_send_msg(self):
        id_message = str(uuid4())
        ch = self.sk.contacts.contact("andriy5852").chat
        ch.sendMsg(id_message)

        results = ch.getMsgs()
        self.assertEqual(id_message, results[0].content)
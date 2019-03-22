from django.test import TestCase
from django.contrib.auth import get_user_model


class ProvidersTests(TestCase):

    def setUp(self):
        get_user_model().objects.create_user(username='test', password='test')
        self.client.login(username='test', password='test')


    def test_can_list_avaliable_providers(self):
        resp = self.client.get('/api/providers/get_avaliable_providers/')
        import ipdb; ipdb.set_trace()

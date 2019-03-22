import fbchat

class FacebookProvider:

    _required_credentials = {
        'username': 'text',
        'password': 'password',
    }

    client = None

    @classmethod
    def login(cls, **credentials):
        username = credentials['username']
        password = credentials['password']

        cls.client = fbchat.Client(username, password)

from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    async def login(self, data):
        pass

    @abstractmethod
    async def get_required_credentials(self):
        pass

    @abstractmethod
    async def am_i_logged(self, data):
        pass

    @abstractmethod
    async def post_login_action(self, data):
        pass

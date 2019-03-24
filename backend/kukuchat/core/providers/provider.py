from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def login(self, **kwargs):
        pass

    @abstractmethod
    def get_required_credentials(self):
        pass

    @abstractmethod
    def is_logged_in(self):
        pass

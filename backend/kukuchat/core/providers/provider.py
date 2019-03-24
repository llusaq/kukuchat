from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @classmethod
    @abstractmethod
    def login(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def get_required_credentials(cls):
        pass

import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser

from jsonfield import JSONField


def get_random_seq():
    return secrets.token_hex(125)


class User(AbstractUser):
    credentials = JSONField(default={})
    temp_dir = models.CharField(max_length=255, default=get_random_seq)

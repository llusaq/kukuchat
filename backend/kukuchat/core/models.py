import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser

from jsonfield import JSONField


def get_random_seq():
    return secrets.token_hex(20)


class User(AbstractUser):
    credentials = JSONField(default={})
    temp_dir = models.CharField(max_length=255, default=get_random_seq, unique=True)


class Chat(models.Model):
    name = models.CharField(max_length=255)


class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    provider = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    class Meta:
        unique_together = 'provider', 'uid'

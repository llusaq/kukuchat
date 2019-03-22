from django.db import models
from django.contrib.auth.models import AbstractUser

from jsonfield import JSONField


class User(AbstractUser):
    credentials = JSONField(default={})

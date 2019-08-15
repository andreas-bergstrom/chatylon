from django.contrib.auth.models import AbstractUser

from accounts.managers import UserManager
from chat.models import Thread


class CustomUser(AbstractUser):
    objects = UserManager()
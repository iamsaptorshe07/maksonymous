from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Messenger(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    msg = models.TextField()
    reciever = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rcvr')
    datetime = models.DateTimeField(auto_now_add=True)

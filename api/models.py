from django.db import models
from django.contrib.auth.models import User
import string
import random


def generate_unique_code():
    """
    Generates unique Room code
    """
    length = 6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return code


class Room(models.Model):
    """
    Contains information about all virtual music rooms.
    Fields:
        * room code (CharField)
        * host (User)
        * guest_can_pause (Boolean)
        * votes_to_skip (Integer)
        * created_at (DateTimeField)
    """
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_user_name(self):
        """
        Returns name of the host
        """
        return self.host.username

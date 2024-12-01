from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField('email address', unique = True)
    phone_no = models.CharField(max_length = 10, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    firstName = models.CharField(max_length=100, blank=False, null=False)
    lastName = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)

    REQUIRED_FIELDS = ["firstName", "lastName", "email"]

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
        }

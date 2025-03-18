from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    role = models.IntegerField(default=0, blank=False, null=False)
    registration_date = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ["firstName", "lastName", "email"]

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "role": self.role,
            "registrationDate": self.registration_date,
        }

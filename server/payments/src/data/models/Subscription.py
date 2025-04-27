from django.db import models
from users.models import User, Address


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    stripe_id = models.TextField(default="")

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.to_json(),
            "billing_address": self.billing_address.to_json(),
            "items": [item.to_json() for item in self.items.all()],
        }

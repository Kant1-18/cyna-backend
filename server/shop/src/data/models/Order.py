from django.db import models
from users.models import User
from users.models import Address


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, blank=False, null=False)
    shipping_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="shipping_address"
    )
    billing_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="billing_address"
    )
    recurrence = models.IntegerField(default=0, blank=False, null=False)

    def to_json(self):
        return {
            "id": self.id,
            "status": self.status,
            "shippingAddress": (
                self.shipping_address.to_json() if self.shipping_address else None
            ),
            "billingAddress": (
                self.billing_address.to_json() if self.billing_address else None
            ),
            "recurrence": self.recurrence,
            "items": [item.to_json() for item in self.items.all()],
        }

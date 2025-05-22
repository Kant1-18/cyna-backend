from django.db import models
from payments.models import PaymentMethod
from users.models import User, Address


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True
    )
    stripe_id = models.TextField(default="")
    recurrence = models.IntegerField(default=0)

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.to_json(),
            "billingAddress": self.billing_address.to_json(),
            "paymentMethod": self.payment_method.to_json(),
            "recurrence": self.recurrence,
            "items": [item.to_json() for item in self.items.all()],
        }

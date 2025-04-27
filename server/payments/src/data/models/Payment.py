from django.db import models
from shop.models import Order
from payments.models import PaymentMethod, Subscription


class Payment(models.Model):
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True
    )
    status = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)

    def to_json(self):
        return {
            "id": self.id,
            "payment_method": (
                self.payment_method.to_json() if self.payment_method else None
            ),
            "status": self.status,
            "amount": self.amount,
            "order": self.order.to_json() if self.order else None,
            "subscription": self.subscription.to_json() if self.subscription else None,
        }

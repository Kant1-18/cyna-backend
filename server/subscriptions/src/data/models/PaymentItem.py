from django.db import models
from subscriptions.models import Subscription, Payment


class PaymentItem(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="payment_items"
    )

    def to_json(self):
        return {
            "id": self.id,
            "subscription": self.subscription.to_json(),
            "payment": self.payment.to_json(),
        }

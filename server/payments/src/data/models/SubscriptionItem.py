from django.db import models
from payments.models import Subscription
from shop.models import OrderItem


class SubscriptionItem(models.Model):
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="items"
    )
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

    def to_json(self):
        return {
            "id": self.id,
            "subscriptionId": self.subscription.id,
            "orderItem": self.order_item.to_json(),
        }

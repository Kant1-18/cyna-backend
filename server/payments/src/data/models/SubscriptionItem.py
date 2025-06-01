from django.db import models
from payments.models import Subscription
from shop.models import OrderItem


class SubscriptionItem(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="items")
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    stripe_item_id = models.CharField(max_length=255, unique=True)
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end   = models.DateTimeField(null=True, blank=True)
    price_id = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        return {
            "id": self.id,
            "subscriptionId": self.subscription.id,
            "orderItem": self.order_item.to_json(),
            "stripeItemId": self.stripe_item_id,
            "currentPeriodStart": int(self.current_period_start.timestamp()) if self.current_period_start else None,
            "currentPeriodEnd": int(self.current_period_end.timestamp()) if self.current_period_end else None,
            "priceId": self.price_id,
            "quantity": self.quantity,
        }

from django.db import models
from shop.models import OrderItem


class Subscription(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    recurrence = models.BooleanField(default=False)

    def to_json(self):
        return {
            "id": self.id,
            "order_item": self.order_item.to_json(),
            "status": self.status,
            "recurrence": self.recurrence,
        }

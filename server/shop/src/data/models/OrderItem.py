from django.db import models
from shop.models import Product
from shop.models import Order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=False, null=False)

    def to_json(self):
        return {
            "id": self.id,
            "product": self.product.id,
            "quantity": self.quantity,
        }

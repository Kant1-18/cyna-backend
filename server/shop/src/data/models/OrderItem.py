from django.db import models
from shop.models import Product
from shop.models import Order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=False, null=False)
    recurring = models.IntegerField(default=0, blank=False, null=False)
    price_at_sale = models.IntegerField(default=None, null=True)

    def save(self, *args, **kwargs):
        if self.price_at_sale is None and self.product.id:
            self.price_at_sale = self.product.price
        super().save(*args, **kwargs)

    def to_json(self):
        return {
            "id": self.id,
            "product": self.product.to_json_admin(),
            "quantity": self.quantity,
            "recurring": self.recurring,
            "priceAtSale": self.price_at_sale
        }

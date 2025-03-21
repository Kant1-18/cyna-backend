from django.db import models
from shop.src.data.models.Product import Product


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    percentage = models.IntegerField(default=0, blank=False, null=False)
    discount_price = models.IntegerField(default=0, blank=False, null=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=False)

    def to_json(self):
        return {
            "id": self.id,
            "product": self.product.to_json(),
            "percentage": self.percentage,
            "discount_price": self.discount_price,
            "start_date": self.start_date.timestamp(),
            "end_date": self.end_date.timestamp(),
        }

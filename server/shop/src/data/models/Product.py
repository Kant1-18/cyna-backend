from django.db import models
from shop.src.data.models.Category import Category


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, blank=False, null=False)
    base_price = models.IntegerField(default=0, blank=False, null=False)
    price = models.IntegerField(default=0, blank=False, null=False)
    discount_order = models.IntegerField(default=0, blank=False, null=False)
    discount_percentage = models.IntegerField(default=0, blank=False, null=False)
    image1 = models.TextField(null=True)
    image2 = models.TextField(null=True)
    image3 = models.TextField(null=True)

    def to_json(self):
        return {
            "category": self.category.to_json(),
            "status": self.status,
            "base_price": self.base_price,
            "price": self.price,
            "discount_order": self.discount_order,
            "discount_percentage": self.discount_percentage,
            "image1": self.image1,
            "image2": self.image2,
            "image3": self.image3,
        }

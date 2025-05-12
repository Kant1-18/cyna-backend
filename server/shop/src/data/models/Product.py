from django.db import models
from shop.src.data.models.Category import Category
import json


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField(null=True)
    type = models.IntegerField(default=0)
    status = models.IntegerField(default=0, blank=False, null=False)
    base_price = models.IntegerField(default=0, blank=False, null=True)
    price = models.IntegerField(default=0, blank=False, null=True)
    discount_order = models.IntegerField(default=0, blank=False, null=False)
    discount_percentage = models.IntegerField(default=0, blank=False, null=False)
    image1 = models.TextField(null=True)
    image2 = models.TextField(null=True)
    image3 = models.TextField(null=True)
    stripe_id = models.TextField(default="")
    stripe_monthly_price_id = models.TextField(null=True)
    stripe_yearly_price_id = models.TextField(null=True)

    # self.base_price * (1 - self.discount_percentage / 100)

    def to_json_single(self, details):
        return {
            "id": self.id,
            "category": self.category.to_json(details.locale),
            "name": self.name,
            "type": self.type,
            "slides": [
                self.image1,
                self.image2,
                self.image3,
            ],
            "basePrice": self.base_price,
            "price": self.price,
            "status": self.status,
            "discountOrder": self.discount_order,
            "discountPercentage": self.discount_percentage,
            "details": details.to_json(),
        }

    def to_json_all(self):
        return {
            "id": self.id,
            "category": self.category.to_json(),
            "name": self.name,
            "type": self.type,
            "basePrice": self.base_price,
            "price": self.price,
            "status": self.status,
            "discountOrder": self.discount_order,
            "discountPercentage": self.discount_percentage,
            "slides": [
                self.image1,
                self.image2,
                self.image3,
            ],
            "details": [detail.to_json() for detail in self.details.all()],
        }

    def to_json_admin(self):
        return {
            "id": self.id,
            "category": self.category.to_json(),
            "name": self.name,
            "type": self.type,
            "basePrice": self.base_price,
            "price": self.price,
            "status": self.status,
            "discountOrder": self.discount_order,
            "discountPercentage": self.discount_percentage,
            "slides": [
                self.image1,
                self.image2,
                self.image3,
            ],
        }

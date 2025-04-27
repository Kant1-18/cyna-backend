from django.db import models
from shop.src.data.models.Category import Category


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField(null=True)
    status = models.IntegerField(default=0, blank=False, null=False)
    base_price = models.IntegerField(default=0, blank=False, null=False)
    price = models.IntegerField(default=0, blank=False, null=True)
    discount_order = models.IntegerField(default=0, blank=False, null=False)
    discount_percentage = models.IntegerField(default=0, blank=False, null=False)
    image1 = models.TextField(null=True)
    image2 = models.TextField(null=True)
    image3 = models.TextField(null=True)
    stripe_id = models.TextField()
    stripe_monthly_price_id = models.TextField(null=True)
    stripe_yearly_price_id = models.TextField(null=True)

    def to_json(self, details):
        if self.price == None:
            self.price = (self.base_price * self.discount_percentage) / 100
        return {
            "id": self.id,
            "category": self.category.to_json(),
            "name": self.name,
            "slides": [
                self.image1,
                self.image2,
                self.image3,
            ],
            "description": {
                "title": details.description_title,
                "text": details.description_text,
            },
            "benefits": [benefit for benefit in details.benefits.split(",")],
            "functionalities": [
                functionality for functionality in details.functionalities.split(",")
            ],
            "specifications": [
                specification for specification in details.specifications.split(",")
            ],
            "price": self.price,
            "status": self.status,
            "discountOrder": self.discount_order,
            "discountPercentage": self.discount_percentage,
        }

    def to_json_admin(self):
        return {
            "id": self.id,
            "category": self.category.to_json(),
            "name": self.name,
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

from django.db import models
from shop.src.data.models.Category import Category

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(null=False)
    status = models.IntegerField(default=0, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    image = models.TextField()
    discount = models.IntegerField(default=0, blank=False, null=False)
    discount_order = models.IntegerField(default=0, blank=False, null=False)
    top_order = models.IntegerField(default=0, blank=False, null=False)
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "status": self.status,
            "category": self.category.to_json(),
            "image": self.image,
            "discount": self.discount,
            "discount_order": self.discount_order,
            "top_order": self.top_order,
            "discountPrice": self.price - (self.price * self.discount / 100)
        }

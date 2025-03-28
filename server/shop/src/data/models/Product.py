from django.db import models
from shop.src.data.models.Category import Category


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(null=False)
    status = models.IntegerField(default=0, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.TextField()
    top_order = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "status": self.status,
            "category": self.category.to_json(),
            "image": self.image,
            "top_order": self.top_order,
        }

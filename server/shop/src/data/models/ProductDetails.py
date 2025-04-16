from django.db import models
from shop.src.data.models.Product import Product


class ProductDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    locale = models.CharField(max_length=5, default="en")
    description_title = models.TextField(null=False)
    description_text = models.TextField(null=False)
    benefits = models.JSONField()
    functionalities = models.JSONField()
    specifications = models.JSONField()

    def to_json(self):
        return {
            "id": self.id,
            "locale": self.locale,
            "description_title": self.description_title,
            "description_text": self.description_text,
            "benefits": self.benefits,
            "functionalities": self.functionalities,
            "specifications": self.specifications,
        }

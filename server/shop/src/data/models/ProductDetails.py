from django.db import models
from shop.src.data.models.Product import Product
import json


class ProductDetails(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="details"
    )
    locale = models.CharField(max_length=5, default="en")
    description_title = models.TextField(null=False)
    description_text = models.TextField(null=False)
    benefits = models.TextField()
    functionalities = models.TextField()
    specifications = models.TextField()

    def to_json(self):
        return {
            "id": self.id,
            "locale": self.locale,
            "descriptionTitle": self.description_title,
            "descriptionText": self.description_text,
            "benefits": json.loads(self.benefits),
            "functionalities": json.loads(self.functionalities),
            "specifications": json.loads(self.specifications),
        }

from django.db import models
from shop.models import Category


class CategoryLocale(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="locales"
    )
    locale = models.TextField(null=False)
    name = models.TextField(null=False)

    def to_json(self):
        return {
            "id": self.id,
            "locale": self.locale,
            "name": self.name,
        }

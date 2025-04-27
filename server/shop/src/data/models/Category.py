from django.db import models


class Category(models.Model):

    def to_json(self, locale: str = "en"):
        return {
            "id": self.id,
            "name": self.locales.get(locale=locale).name,
        }

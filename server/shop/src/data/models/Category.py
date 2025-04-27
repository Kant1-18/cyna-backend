from django.db import models


class Category(models.Model):
    global_name = models.TextField(default="")

    def to_json(self, locale: str = "en"):
        return {
            "id": self.id,
            "global_name": self.global_name,
            "locale_name": (
                self.locales.get(locale=locale).name
                if self.locales.filter(locale=locale).exists()
                else self.global_name
            ),
        }

    def to_json_all_locales(self):
        return {
            "id": self.id,
            "global_name": self.global_name,
            "locales": [locale.to_json() for locale in self.locales.all()],
        }

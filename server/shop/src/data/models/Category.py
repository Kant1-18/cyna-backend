from django.db import models


class Category(models.Model):
    global_name = models.TextField(default="")

    def to_json(self, locale: str = "en"):
        locale_obj = self.locales.get(locale=locale)
        return {
            "id": self.id,
            "globalName": self.global_name,
            "localeId": locale_obj.id,
            "locale": locale_obj.locale,
            "localeName": locale_obj.name,
        }

    def to_json_all_locales(self):
        return {
            "id": self.id,
            "globalName": self.global_name,
            "locales": [locale.to_json() for locale in self.locales.all()],
        }

    def to_json_global(self):
        return {
            "id": self.id,
            "globalName": self.global_name,
        }

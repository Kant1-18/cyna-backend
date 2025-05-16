from django.db import models


class HomeText(models.Model):
    locale = models.CharField(max_length=2, unique=True)
    text = models.TextField()

    def to_json(self):
        return {
            "locale": self.locale,
            "text": self.text,
        }

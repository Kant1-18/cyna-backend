from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name

    def to_json(self):
        return {"id": self.id, "name": self.name}

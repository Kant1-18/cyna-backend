from django.db import models


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    stripe_code = models.CharField(max_length=255)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "stripeCode": self.stripe_code,
        }

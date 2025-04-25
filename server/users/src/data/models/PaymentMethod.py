from django.db import models
from users.src.data.models.User import User


class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    iban = models.CharField(max_length=34)

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.to_json(),
            "number": self.number,
            "expiration_date": self.expiration_date,
            "iban": self.iban,
        }

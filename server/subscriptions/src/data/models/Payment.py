from django.db import models
from users.models import PaymentMethod


class Payment(models.Model):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    amount = models.IntegerField()

    def to_json(self):
        return {
            "id": self.id,
            "payment_method": self.payment_method.to_json(),
            "status": self.status,
            "amount": self.amount,
        }

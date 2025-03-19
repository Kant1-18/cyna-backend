from django.db import models
from users.src.data.models.User import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, blank=False, null=False)
    
    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.to_json(),
            "status": self.status,
            "products": [order_products.to_json() for order_products in self.order_products.all()]
        }

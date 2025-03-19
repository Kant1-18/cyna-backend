from django.db import models
from shop.src.data.models.Product import Product
from users.src.data.models.User import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.to_json(),
            "products": [
                cart_products.to_json() for cart_products in self.cart_products.all()
            ],
        }

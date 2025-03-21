from django.db import models
from shop.src.data.models.Cart import Cart
from shop.src.data.models.Product import Product


class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_products"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def to_json(self):
        return {"product": self.product.to_json(), "quantity": self.quantity}

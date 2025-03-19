from django.db import models
from shop.src.data.models.Order import Order
from shop.src.data.models.Product import Product

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    
    def to_json(self):
        return {
            "product": self.product.to_json(),
            "quantity": self.quantity
        }

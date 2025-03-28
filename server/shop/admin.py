from django.contrib import admin
from shop.models import (
    Product,
    Category,
    Discount,
    Cart,
    CartProduct,
    Order,
    OrderProduct,
)

admin.site.register(Product)
admin.site.register(Category)

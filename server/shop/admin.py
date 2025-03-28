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
admin.site.register(Discount)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(OrderProduct)

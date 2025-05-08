from django.urls import path
from django.contrib import admin
from ninja import NinjaAPI
from users.src.routes.AuthUrls import router as auth_router
from users.src.routes.UserUrls import router as user_router
from users.src.routes.AddressUrls import router as address_router

from shop.src.routes.CategoryUrls import router as category_router
from shop.src.routes.ProductUrls import router as product_router
from shop.src.routes.OrderUrls import router as order_router

from tickets.src.routes.TicketUrls import router as ticket_router

from payments.src.routes.PaymentMethodUrls import router as payment_method_router
from payments.src.routes.SubscriptionUrls import router as subscription_router


api = NinjaAPI()

api.add_router("auth", auth_router)
api.add_router("users", user_router)
api.add_router("addresses", address_router)

api.add_router("categories", category_router)
api.add_router("products", product_router)
api.add_router("orders", order_router)

api.add_router("tickets", ticket_router)

api.add_router("payment-methods", payment_method_router)
api.add_router("subscriptions", subscription_router)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

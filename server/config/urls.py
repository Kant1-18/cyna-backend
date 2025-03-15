from django.urls import path
from ninja import NinjaAPI
from users.src.routes.AuthUrls import router as auth_router
from users.src.routes.UserUrls import router as user_router

api = NinjaAPI()

api.add_router("/auth", auth_router)
api.add_router("/users", user_router)

urlpatterns = [
    path("api/", api.urls),
]

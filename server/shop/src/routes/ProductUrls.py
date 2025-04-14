from shop.src.data.models.Product import Product
from shop.src.controllers.ProductControl import ProductControl
from ninja import Router, ModelSchema, Schema
from ninja.errors import HttpError
from ninja import File, Form, UploadedFile
from ninja_jwt.authentication import JWTAuth

router = Router()


class ProductSchema(ModelSchema):
    class Meta:
        model = Product
        fields = "__all__"


...

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


class ProductUpdateSchema(Schema):
    id: int
    name: str
    description: str
    price: int
    status: int
    categoryId: int


# @router.post("/add", auth=JWTAuth())
# def add(
#     request,
#     name: str = Form(...),
#     description: str = Form(...),
#     price: int = Form(...),
#     status: int = Form(...),
#     categoryId: int = Form(...),
#     image: UploadedFile = File(...),
# ) -> Product | HttpError:
#     return ProductControl.add(
#         request,
#         {
#             "name": name,
#             "description": description,
#             "price": price,
#             "status": status,
#             "categoryId": categoryId,
#             "image": image,
#         },
#     )

...

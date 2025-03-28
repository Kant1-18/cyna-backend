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


class UpdateSchema(Schema):
    id: int
    name: str
    description: str
    price: int
    status: int
    categoryId: int


@router.post("/add", auth=JWTAuth())
def add(
    request,
    name: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    status: int = Form(...),
    categoryId: int = Form(...),
    image: UploadedFile = File(...),
) -> Product | HttpError:
    return ProductControl.add(
        request,
        {
            "name": name,
            "description": description,
            "price": price,
            "status": status,
            "categoryId": categoryId,
            "image": image,
        },
    )


@router.get("/get/{id}", auth=JWTAuth())
def get(request, id: int) -> Product | HttpError:
    return ProductControl.get(id)


@router.get("/getAll", auth=JWTAuth())
def get_all(request) -> list[Product] | HttpError:
    return ProductControl.get_all()


@router.get("/getAllByCategory/{categoryId}", auth=JWTAuth())
def get_all_by_category(request, categoryId: int) -> list[Product] | HttpError:
    return ProductControl.get_all_by_category(categoryId)


@router.put("/update", auth=JWTAuth())
def update(request, data: UpdateSchema) -> Product | HttpError:
    return ProductControl.update(request, data)


@router.put("/updateImage", auth=JWTAuth())
def update_image(
    request, id: int = Form(...), image: UploadedFile = File(...)
) -> bool | HttpError:
    return ProductControl.update_image(request, {"id": id, "image": image})


@router.delete("/delete/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return ProductControl.delete(request, id)

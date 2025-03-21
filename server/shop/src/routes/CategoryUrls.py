from ninja import Router, ModelSchema, Schema
from ninja_jwt.authentication import JWTAuth
from shop.src.data.models.Category import Category
from shop.src.controllers.CategoryControl import CategoryControl
from ninja.errors import HttpError

router = Router()


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = "__all__"


class AddCategorySchema(Schema):
    name: str


class UpdateCategorySchema(Schema):
    id: int
    name: str


@router.post("/add", auth=JWTAuth())
def add(request, data: AddCategorySchema) -> Category | HttpError:
    return CategoryControl.add(request, data)


@router.get("/get/{id}", auth=JWTAuth())
def get(request, id: int) -> Category | HttpError:
    return CategoryControl.get(id)


@router.get("/getByName/{name}", auth=JWTAuth())
def get_by_name(request, name: str) -> Category | HttpError:
    return CategoryControl.get_by_name(name)


@router.get("/getAll", auth=JWTAuth())
def get_all(request) -> list[Category] | HttpError:
    return CategoryControl.get_all()


@router.put("/update", auth=JWTAuth())
def update(request, data: UpdateCategorySchema) -> Category | HttpError:
    return CategoryControl.update(request, data)


@router.delete("/delete/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return CategoryControl.delete(request, id)

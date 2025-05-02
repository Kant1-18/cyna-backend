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
    globalName: str


class AddLocaleCategorySchema(Schema):
    id: int
    locale: str
    name: str


class UpdateCategorySchema(Schema):
    id: int
    globalName: str


class UpdateCategoryLocaleSchema(Schema):
    id: int
    locale: str
    name: str


@router.post("/add", auth=JWTAuth())
def add(request, data: AddCategorySchema) -> Category | HttpError:
    return CategoryControl.add(request, data)


@router.post("/add-locale", auth=JWTAuth())
def add_locale(request, data: AddLocaleCategorySchema) -> Category | HttpError:
    return CategoryControl.add_locale(request, data)


@router.get("/get/{id}/{locale}", auth=JWTAuth())
def get(request, id: int, locale: str) -> Category | HttpError:
    return CategoryControl.get(id, locale)


@router.get("/get-by-global-name/{gloabal_name}", auth=JWTAuth())
def get_by_global_name(request, gloabal_name: str) -> Category | HttpError:
    return CategoryControl.get_by_global_name(gloabal_name)


@router.get("/get-all", auth=JWTAuth())
def get_all(request) -> list[Category] | HttpError:
    return CategoryControl.get_all()


@router.get("/get-all-categories/{locale}", auth=JWTAuth())
def get_all_categories(request, locale: str) -> list[Category] | HttpError:
    return CategoryControl.get_all(locale=locale)


@router.get("/get-all-locales", auth=JWTAuth())
def get_all_locales(request) -> list[Category] | HttpError:
    return CategoryControl.get_all_locales()


@router.put("/update", auth=JWTAuth())
def update(request, data: UpdateCategorySchema) -> Category | HttpError:
    return CategoryControl.update(request, data)


@router.put("/update-locale", auth=JWTAuth())
def update_locale(request, data: UpdateCategoryLocaleSchema) -> Category | HttpError:
    return CategoryControl.update_locale(request, data)


@router.delete("/delete/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return CategoryControl.delete(request, id)


@router.delete("/delete-locale/{locale_id}", auth=JWTAuth())
def delete_locale(request, locale_id: int) -> bool:
    return CategoryControl.delete_locale(request, locale_id)

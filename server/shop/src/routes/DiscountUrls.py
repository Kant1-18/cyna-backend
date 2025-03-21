from ninja import Router, ModelSchema, Schema
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from shop.src.controllers.DiscountControl import DiscountControl
from shop.src.data.models.Discount import Discount


router = Router()


class DiscountSchema(ModelSchema):
    class Meta:
        model = Discount
        fields = "__all__"


class AddDiscountSchema(Schema):
    productId: int
    percentage: int
    endDate: float


class UpdateDiscountSchema(Schema):
    id: int
    percentage: int
    endDate: float


@router.post("/add", auth=JWTAuth())
def add(request, data: AddDiscountSchema) -> Discount | HttpError:
    return DiscountControl.add(request, data)


@router.get("/get/{id}", auth=JWTAuth())
def get(request, id: int) -> Discount | HttpError:
    return DiscountControl.get(id)


@router.get("/getActiveByProduct/{productId}", auth=JWTAuth())
def get_active_by_product(request, productId: int) -> Discount | HttpError:
    return DiscountControl.get_active_by_product(productId)


@router.get("/getAll", auth=JWTAuth())
def get_all(request) -> list[Discount] | HttpError:
    return DiscountControl.get_all()


@router.get("/getAllActive", auth=JWTAuth())
def get_all_active(request) -> list[Discount] | HttpError:
    return DiscountControl.get_all_active()


@router.put("/update", auth=JWTAuth())
def update(request, data: UpdateDiscountSchema) -> Discount | HttpError:
    return DiscountControl.update(request, data)


@router.delete("/delete/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool | None:
    return DiscountControl.delete(request, id)

from ninja import Router, ModelSchema, Schema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from users.src.data.models.Address import Address
from users.src.controllers.AddressControl import AddressControl

router = Router()


class AddressSchema(ModelSchema):
    class Meta:
        model = Address
        fields = "__all__"


class AddSchema(Schema):
    type: int
    street: str
    number: str
    complement: str
    zipCode: str
    city: str
    region: str
    country: str


class AddressUpdateSchema(Schema):
    id: int
    type: int
    street: str
    number: str
    complement: str
    zipCode: str
    city: str
    region: str
    country: str


@router.post("/add", auth=JWTAuth())
def add(request, data: AddSchema) -> Address | HttpError:
    return AddressControl.add(request, data)


@router.get("/get/{id}", auth=JWTAuth())
def get(request, id: int) -> Address | HttpError:
    return AddressControl.get(id)


@router.get("/get-all", auth=JWTAuth())
def get_all_by_user(request) -> list[Address] | HttpError:
    return AddressControl.get_all_by_user(request)


@router.put("/update", auth=JWTAuth())
def update(request, data: AddressUpdateSchema) -> Address | HttpError:
    return AddressControl.update(data)


@router.delete("/delete/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return AddressControl.delete(id)

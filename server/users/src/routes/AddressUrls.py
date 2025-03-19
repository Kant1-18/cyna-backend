from ninja import Router, ModelSchema, Schema
from ninja_jwt.authentication import JWTAuth
from typing import Optional, List
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


class UpdateSchema(Schema):
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
def add(request, data: AddSchema) -> Optional[Address]:
    return AddressControl.add(request, data)


@router.get("/get/{id}", auth=JWTAuth())
def get(request, id: int) -> Optional[Address]:
    return AddressControl.get(id)


@router.get("/getAll", auth=JWTAuth())
def get_all_by_user(request) -> Optional[List[Address]]:
    return AddressControl.get_all_by_user(request)


@router.put("/update", auth=JWTAuth())
def update(request, data: UpdateSchema) -> Optional[Address]:
    return AddressControl.update(data)


@router.delete("/delete/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return AddressControl.delete(id)

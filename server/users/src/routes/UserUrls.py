from ninja import Router, ModelSchema, Schema
from ninja_jwt.authentication import JWTAuth
from typing import Optional
from users.src.controllers.UserControl import UsersControl
from users.src.data.models.User import User

router = Router()


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"


class UpdateSchema(Schema):
    firstName: str
    lastName: str
    email: str
    role: int


class UpdatePasswordSchema(Schema):
    previousPassword: str
    newPassword: str
    confirmNewPassword: str


@router.get("/get/{id}", auth=JWTAuth())
def get(request, id: int) -> Optional[User]:
    return UsersControl.get(id)


@router.get("/getByEmail/{email}", auth=JWTAuth())
def get_by_email(request, email: str) -> Optional[User]:
    return UsersControl.get_by_email(email)


@router.put("/update", auth=JWTAuth())
def update(request, data: UpdateSchema) -> Optional[User]:
    return UsersControl.update(data)


@router.put("/updatePassword", auth=JWTAuth())
def update_password(request, data: UpdatePasswordSchema) -> Optional[User]:
    return UsersControl.update_password(data)


@router.delete("/delete/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return UsersControl.delete(id)

from ninja import Router, ModelSchema, Schema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from users.src.controllers.UserControl import UsersControl
from users.src.data.models.User import User

router = Router()


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"


class UserAddAdminSchema(Schema):
    firstName: str
    lastName: str
    email: str
    password: str
    confirmPassword: str


class UserUpdateSchema(Schema):
    firstName: str
    lastName: str
    email: str


class UpdatePasswordSchema(Schema):
    previousPassword: str
    newPassword: str
    confirmNewPassword: str


@router.post("/add-admin", auth=JWTAuth())
def add_admin(request, data: UserAddAdminSchema) -> User | HttpError:
    return UsersControl.add_admin(request, data)


@router.get("/get/{id}", auth=JWTAuth())
def get(request, id: int) -> User | HttpError:
    return UsersControl.get(id)


@router.get("/get-by-email/{email}", auth=JWTAuth())
def get_by_email(request, email: str) -> User | HttpError:
    return UsersControl.get_by_email(email)


@router.put("/update", auth=JWTAuth())
def update(request, data: UserUpdateSchema) -> User | HttpError:
    return UsersControl.update(request, data)


@router.put("/update-password", auth=JWTAuth())
def update_password(request, data: UpdatePasswordSchema) -> User | HttpError:
    return UsersControl.update_password(request, data)


@router.delete("/delete/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return UsersControl.delete(id)

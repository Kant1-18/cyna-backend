from ninja import Router, Schema
from users.src.controllers.AuthControl import AuthControl
from ninja_jwt.authentication import JWTAuth

router = Router()


class RegisterSchema(Schema):
    firstName: str
    lastName: str
    email: str
    password: str
    confirmPassword: str


class LoginSchema(Schema):
    email: str
    password: str


@router.post("/register")
def register(request, data: RegisterSchema):
    return AuthControl.register(data)


@router.post("/login")
def login(request, data: LoginSchema):
    return AuthControl.login(data)


@router.post("/refresh")
def refresh(request):
    return AuthControl.refresh(request)


@router.get("/me", auth=JWTAuth())
def me(request):
    return AuthControl.me(request)


@router.post("/logout")
def logout(request):
    return AuthControl.logout(request)

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


class TokenShema(Schema):
    token: str


@router.post("/register")
def register(request, data: RegisterSchema):
    return AuthControl.register(data)


@router.post("/login")
def login(request, data: LoginSchema):
    return AuthControl.login(data)


@router.post("/refresh", auth=JWTAuth())
def refresh(request, data: TokenShema):
    return AuthControl.refresh(data)


@router.get("/me", auth=JWTAuth())
def me(request):
    return AuthControl.me(request)

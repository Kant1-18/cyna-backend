from ninja.errors import HttpError
from ninja import Router, ModelSchema, Schema
from home.models import HomeText
from home.src.controllers.HomeTextControl import HomeTextControl
from ninja_jwt.authentication import JWTAuth

router = Router()


class HomeTextSchema(ModelSchema):
    class Meta:
        model = HomeText
        fields = "__all__"


class HomeTextSchema(Schema):
    locale: str
    text: str


@router.post("", auth=JWTAuth())
def add(request, data: HomeTextSchema) -> HomeText | HttpError:
    return HomeTextControl.add(request, data)


@router.get("")
def get_all(request) -> list[HomeText] | HttpError:
    return HomeTextControl.get_all()


@router.get("/{locale}")
def get(request, locale: str) -> HomeText | HttpError:
    return HomeTextControl.get(request, locale)


@router.put("", auth=JWTAuth())
def update(request, data: HomeTextSchema) -> HomeText | HttpError:
    return HomeTextControl.update(request, data)

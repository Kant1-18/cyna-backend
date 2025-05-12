from ninja import Router, Schema
from payments.src.controllers.CheckingControl import CheckingControl
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError

router = Router()


class CheckingSchema(Schema):
    orderId: int
    paymentMethodId: int


@router.post("", auth=JWTAuth())
def checking(request, data: CheckingSchema) -> tuple[dict, dict] | HttpError:
    return CheckingControl.checking(request, data)

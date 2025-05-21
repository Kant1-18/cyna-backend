from ninja import Router, ModelSchema, Schema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from payments.src.data.models.PaymentMethod import PaymentMethod
from payments.src.controllers.PaymentMethodControl import PaymentMethodControl

router = Router()


class PaymentMethodSchema(ModelSchema):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class AddPaymentMethodSchema(Schema):
    name: str
    stripeCode: str


class UpdatePaymentMethodSchema(Schema):
    id: int
    name: str
    stripeCode: str


@router.post("", auth=JWTAuth())
def add_payment_method(
    request, data: AddPaymentMethodSchema
) -> PaymentMethod | HttpError:
    return PaymentMethodControl.add(request, data)


@router.get("/{id}", auth=JWTAuth())
def get_payment_method(request, id: int) -> PaymentMethod | HttpError:
    return PaymentMethodControl.get(request, id)


@router.get("", auth=JWTAuth())
def get_all_payment_methods(request) -> list[PaymentMethod] | HttpError:
    return PaymentMethodControl.get_all(request)


@router.put("", auth=JWTAuth())
def update_payment_method(
    request, data: UpdatePaymentMethodSchema
) -> PaymentMethod | HttpError:
    return PaymentMethodControl.update(request, data)


@router.delete("/{id}", auth=JWTAuth())
def delete_payment_method(request, id: int) -> bool:
    return PaymentMethodControl.delete(request, id)

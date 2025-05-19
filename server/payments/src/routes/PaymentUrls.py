from ninja.errors import HttpError
from ninja import Router, ModelSchema, Schema
from payments.models import Payment
from payments.src.controllers.PaymentControl import PaymentControl
from ninja_jwt.authentication import JWTAuth

router = Router()


class PaymentSchema(ModelSchema):
    class Meta:
        model = Payment
        fields = "__all__"


class AddPaymentSchema(Schema):
    paymentMethodId: int
    amount: int
    status: int
    orderId: int | None
    subscriptionId: int | None


class UpdateStatusSchema(Schema):
    id: int
    status: int


@router.post("", auth=JWTAuth())
def add(request, data: AddPaymentSchema) -> Payment | HttpError:
    return PaymentControl.add(data)


@router.get("", auth=JWTAuth())
def get_all(request) -> list[Payment] | HttpError:
    return PaymentControl.get_all(request)


@router.patch("/status", auth=JWTAuth())
def update_status(request, data: UpdateStatusSchema) -> Payment | HttpError:
    return PaymentControl.update_status(data)


@router.get("/subscription/{subscription_id}", auth=JWTAuth())
def get_by_subscription(request, subscription_id: int) -> Payment | HttpError:
    return PaymentControl.get_by_subscription(request, subscription_id)


@router.get("/order/{order_id}", auth=JWTAuth())
def get_by_order(request, order_id: int) -> Payment | HttpError:
    return PaymentControl.get_by_order(order_id)


@router.get("/{id}", auth=JWTAuth())
def get(request, id: int) -> Payment | HttpError:
    return PaymentControl.get(id)


@router.delete("/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return PaymentControl.delete(request, id)

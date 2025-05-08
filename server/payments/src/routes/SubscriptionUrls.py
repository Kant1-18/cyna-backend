from ninja.errors import HttpError
from ninja import Router, ModelSchema, Schema
from payments.models import Subscription
from payments.src.controllers.SubscriptionControl import SubscriptionControl
from ninja_jwt.authentication import JWTAuth

router = Router()


class SubscriptionSchema(ModelSchema):
    class Meta:
        model = Subscription
        fields = "__all__"


class AddSubscriptionSchema(Schema):
    billingAddressId: int
    paymentMethodId: int
    recurrence: int
    orderId: int


class UpdateSubscriptionAddressSchema(Schema):
    id: int
    billingAddressId: int


class UpdateSubscriptionStatusSchema(Schema):
    id: int
    status: int


class DeleteSubscriptionItemSchema(Schema):
    id: int
    orderItemId: int


@router.post("", auth=JWTAuth())
def add(request, data: AddSubscriptionSchema) -> Subscription | HttpError:
    return SubscriptionControl.add(request, data)


@router.get("", auth=JWTAuth())
def get_all(request) -> list[Subscription] | HttpError:
    return SubscriptionControl.get_all(request)


@router.get("/my", auth=JWTAuth())
def get_by_user(request) -> Subscription | HttpError:
    return SubscriptionControl.get_my(request)


@router.get("/{user_id}", auth=JWTAuth())
def get_by_user_id(request, user_id: int) -> Subscription | HttpError:
    return SubscriptionControl.get_by_user(request, user_id)


@router.put("/billing-address", auth=JWTAuth())
def update_billing_address(
    request, data: UpdateSubscriptionAddressSchema
) -> Subscription | HttpError:
    return SubscriptionControl.update_billing_address(request, data)


@router.put("/status", auth=JWTAuth())
def update_status(
    request, data: UpdateSubscriptionStatusSchema
) -> Subscription | HttpError:
    return SubscriptionControl.update_status(request, data)


@router.delete("/item", auth=JWTAuth())
def delete_item(request, data: DeleteSubscriptionItemSchema) -> bool:
    return SubscriptionControl.delete_item(request, data)


@router.delete("/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return SubscriptionControl.delete(request, id)

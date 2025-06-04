from ninja.errors import HttpError
from ninja import Router, ModelSchema, Schema, Query
from payments.models import Subscription
from payments.src.controllers.SubscriptionControl import SubscriptionControl
from ninja_jwt.authentication import JWTAuth
from typing import Optional, List

router = Router()


class SubscriptionSchema(ModelSchema):
    class Meta:
        model = Subscription
        fields = "__all__"

class AddSubscriptionSchema(Schema):
    billingAddressId: int
    recurrence: int
    orderId: int


class UpdateSubscriptionAddressSchema(Schema):
    id: int
    billingAddressId: int


class UpdateSubscriptionStatusSchema(Schema):
    id: int
    status: int


class UpdateSubscriptionRecurrenceSchema(Schema):
    id: int
    recurrence: int


class DeleteSubscriptionItemSchema(Schema):
    id: int
    orderItemId: int

class CancelSubscriptionSchema(Schema):
    subscriptionItemStripeId: str
    subscriptionId: int


@router.post("", auth=JWTAuth())
def add(request, data: AddSubscriptionSchema) -> Subscription | HttpError:
    return SubscriptionControl.add(request, data)

@router.post("/cancel", auth=JWTAuth())
def cancel_subscription(request, data: CancelSubscriptionSchema):
    return SubscriptionControl.cancel_subsciption(request, data)


@router.get("", auth=JWTAuth())
def get_all(request) -> list[Subscription] | HttpError:
    return SubscriptionControl.get_all(request)

# quick fix : review code
@router.get("/my", auth=JWTAuth())
def get_by_user(request,  status: str = Query("all")) -> list[Subscription] | HttpError:
    return SubscriptionControl.get_my(request, status)

# changed to fix delete route
@router.get("/user/{user_id}", auth=JWTAuth())
def get_by_user_id(request, user_id: int) -> Subscription | HttpError:
    return SubscriptionControl.get_by_user(request, user_id)


@router.patch("/billing-address", auth=JWTAuth())
def update_billing_address(
    request, data: UpdateSubscriptionAddressSchema
) -> Subscription | HttpError:
    return SubscriptionControl.update_billing_address(data)


@router.patch("/status", auth=JWTAuth())
def update_status(
    request, data: UpdateSubscriptionStatusSchema
) -> Subscription | HttpError:
    return SubscriptionControl.update_status(request, data)


@router.patch("/recurrence", auth=JWTAuth())
def update_recurrence(
    request, data: UpdateSubscriptionRecurrenceSchema
) -> Subscription | HttpError:
    return SubscriptionControl.update_recurrence(data)


@router.delete("/item", auth=JWTAuth())
def delete_item(request, data: DeleteSubscriptionItemSchema) -> bool:
    return SubscriptionControl.delete_item(data)


@router.delete("/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return SubscriptionControl.delete(request, id)

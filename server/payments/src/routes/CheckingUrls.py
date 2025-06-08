from ninja import Router, Schema
from payments.src.controllers.CheckingControl import CheckingControl
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from stripe import stripe
from users.src.services.AuthService import AuthService
from utils.Stripe import StripeUtils

router = Router()


class CheckingSchema(Schema):
    orderId: int
    paymentMethodId: str
    paymentMethodType: str


class CreateSetupSchema(Schema):
    orderId: int


class CreateSetupResponse(Schema):
    intentId: str
    clientSecret: str


class CancelSetupSchema(Schema):
    intentId: str


@router.post("", auth=JWTAuth())
def checking(request, data: CheckingSchema) -> tuple[dict, dict] | HttpError:
    return CheckingControl.checking(request, data)


@router.post("/create-setup-intent", auth=JWTAuth(), response=CreateSetupResponse)
def create_setup_intent(request, data: CreateSetupSchema):
    token = AuthService.get_token(request)
    user = AuthService.get_user_by_access_token(token)

    intent = StripeUtils.create_setup_intent(user, data.orderId)
    return CreateSetupResponse(
        intentId=intent.id,
        clientSecret=intent.client_secret,
    )


# WIP
# Review + split code
@router.post("/cancel-setup-intent", auth=JWTAuth())
def cancel_setup_intent(request, data: CancelSetupSchema):
    try:
        # add id verif
        canceled = stripe.SetupIntent.cancel(data.intentId)
    except stripe.error.StripeError as e:
        raise HttpError(400, f"Cancel failed: {e.user_message}")
    return {"canceled": True}


@router.post("/webhook")
def stripe_webhook(request):
    return CheckingControl.stripe_webhook(request)

from ninja import Router, Schema
import stripe.error
from payments.src.controllers.CheckingControl import CheckingControl
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from stripe import stripe
from users.src.services.AuthService import AuthService
from shop.src.services.OrderService import OrderService
from config.settings import STRIPE_WEBHOOK_SECRET

router = Router()


class CheckingSchema(Schema):
    orderId: int
    paymentMethodId: str

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
    
    intent = stripe.SetupIntent.create(
        customer=user.stripe_id,
        payment_method_types=[
            "card",
            "link",
            "sepa_debit",
        ],
        metadata={"order_id": str(data.orderId)},
    )
    return CreateSetupResponse(
        intentId=intent.id,
        clientSecret=intent.client_secret,
    )

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
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature", "")
    endpoint_secret = STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        raise HttpError(400, f"Webhook error : {str(e)}")
    
    try:
        event_object = event["data"]["object"]
        event_type = event["type"]
        order_id = None

        if event_type.startswith("payment_intent"):
            order_id = event_object.get("metadata", {}).get("order_id")
        if event_type.startswith("invoice"):
            order_id = (event_object.get("metadata", {}).get("order_id"))
            if not order_id:
                order_id = (event_object.get("parent", {}).get("subscription_details", {}).get("metadata", {}).get("order_id"))

        if not order_id:
            print("ignored")
            return {"status": "ignored"}
    
        if event["type"] == "payment_intent.succeeded":
            print("succeeded")
            OrderService.update_order_status(order_id, status=5)
        elif event["type"] == "invoice.paid":
            print("paid")
            OrderService.update_order_status(order_id, status=5)
        elif event["type"] in ("payment_intent.payment_failed", "invoice.payment_failed"):
            print("failed")
            OrderService.update_order_status(order_id, status=2)
        elif event["type"] == "customer.subscription.deleted":
            print("deleted")
            OrderService.update_order_status(order_id, status=3)
    except Exception as e:
        print(f"Error processing webhook {event['type']}: {e}")
        raise HttpError(400, f"Webhook error : {str(e)}")

    return {"status": "success"}
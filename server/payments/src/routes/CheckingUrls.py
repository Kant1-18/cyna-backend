from ninja import Router, Schema
import stripe.error
from payments.src.controllers.CheckingControl import CheckingControl
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from stripe import stripe
from users.src.services.AuthService import AuthService
from shop.src.services.OrderService import OrderService
from config.settings import STRIPE_WEBHOOK_SECRET
from payments.src.services.PaymentMethodService import PaymentMethodService
from payments.src.data.repositories.SubscriptionRepo import SubscriptionRepo
from payments.src.data.repositories.SubscriptionItemRepo import SubscriptionItemRepo
from utils.emails import send_receipt

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

# WIP 
# Review + split code
@router.post("/create-setup-intent", auth=JWTAuth(), response=CreateSetupResponse)
def create_setup_intent(request, data: CreateSetupSchema):
    token = AuthService.get_token(request)
    user = AuthService.get_user_by_access_token(token)

    payment_methods = PaymentMethodService.get_all()
    payment_method_types = []
    if payment_methods:
        payment_method_types = [payment_method.stripe_code for payment_method in payment_methods]
    else:
        payment_method_types = ["card", "link", "sepa_debit"]
    
    intent = stripe.SetupIntent.create(
        customer=user.stripe_id,
        payment_method_types=payment_method_types,
        metadata={"order_id": str(data.orderId)},
    )
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

# WIP 
# Review + split code
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
            print("invoice.paid")
            print("event", event)

            invoice = event_object
            stripe_subscription_id = invoice.get("parent", {}).get("subscription_details", {}).get("subscription", {})
            hosted_invoice_url = invoice.get("hosted_invoice_url")

            try:
                stripe_subscription = stripe.Subscription.retrieve(stripe_subscription_id, expand=["latest_invoice"])
            except Exception as e:
                print(f"Could not retrieve subscription {stripe_subscription_id}: {e}")
                return {"status": "ignored"}
            
            new_status = stripe_subscription["status"]

            OrderService.update_order_status(order_id, status=5)
            subscription = SubscriptionRepo.update_by_stripe_id(
                id=stripe_subscription_id, 
                status=new_status, 
                last_invoice_url=hosted_invoice_url, 
            )

            send_receipt(user_email=invoice.customer_email, subscription=subscription)

            for line in invoice.get("lines", {}).get("data", {}):
                subscription_item_id = line.get("parent", {}).get("subscription_item_details", {}).get("subscription_item")
                new_start = line.get("period", {}).get("start", {})
                new_end = line.get("period", {}).get("end", {})

                SubscriptionItemRepo.update_periods_by_stripe_id(
                    stripe_item_id=subscription_item_id, 
                    new_start=new_start, 
                    new_end=new_end
                )
                

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
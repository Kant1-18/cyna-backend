import stripe.error
from payments.src.services.CheckingService import CheckingService
from utils.CheckInfos import CheckInfos
from ninja.errors import HttpError
from users.src.services.AuthService import AuthService
from shop.src.services.OrderService import OrderService
from shop.src.services.OrderService import OrderService
from config.settings import STRIPE_WEBHOOK_SECRET
from users.src.services.UserService import UserService


class CheckingControl:
    # Review and split code
    @staticmethod
    def checking(request, data) -> dict | HttpError:
        if not CheckInfos.is_positive_int(data.orderId):
            raise HttpError(400, "Invalid order id")
        if not OrderService.is_cart(data.orderId):
            raise HttpError(400, "Order is not a cart")
        order = OrderService.get_order_by_id(data.orderId)
        if order.billing_address is None:
            raise HttpError(400, "Billing address is not set")
        if order.shipping_address is None:
            raise HttpError(400, "Shipping address is not set")

        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)

        payments = CheckingService.checking(
            user,
            order,
            data.paymentMethodId,
            data.paymentMethodType,
        )

        return {"payments": payments}

    # Old method
    # @staticmethod
    # def _checking(request, data) -> tuple[Payment, PaymentIntent] | HttpError:
    #     if not CheckInfos.is_positive_int(data.orderId):
    #         raise HttpError(400, "Invalid order id")

    #     if not OrderService.is_cart(data.orderId):
    #         raise HttpError(400, "Order is not a cart")

    #     order = OrderService.get_order_by_id(data.orderId)
    #     if order.billing_address is None:
    #         raise HttpError(400, "Billing address is not set")

    #     token = AuthService.get_token(request)
    #     user = AuthService.get_user_by_access_token(token)

    #     result, payment_infos, result_type = CheckingService.checking(
    #         user,
    #         order,
    #     )

    #     if result:
    #         if payment_infos:
    #             if result_type == 0:
    #                 return {
    #                     "payment": result.to_json(),
    #                     "paymentIntent": payment_infos,
    #                 }
    #             elif result_type == 1:
    #                 return {
    #                     "subscription": result.to_json(),
    #                     "clientSecret": payment_infos,
    #                 }
    #         else:
    #             if CheckingService.cancel(result.id, result_type):
    #                 raise HttpError(500, "Payment canceled")

    #     raise HttpError(500, "An error occurred while checking the payment")

    @staticmethod
    def stripe_webhook(request):
        payload = request.body
        sig_header = request.headers.get("Stripe-Signature", "")
        endpoint_secret = STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            raise HttpError(400, f"Webhook error : {str(e)}")

        try:
            CheckingService.stripe_webhook_event(event)
        except Exception as e:
            print(f"Error processing webhook {event['type']}: {e}")
            raise HttpError(400, f"Webhook error : {str(e)}")

        return {"status": "success"}

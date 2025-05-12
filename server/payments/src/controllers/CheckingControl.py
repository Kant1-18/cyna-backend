from payments.models import Payment, Subscription
from payments.src.services.CheckingService import CheckingService
from utils.CheckInfos import CheckInfos
from ninja.errors import HttpError
from users.src.services.AuthService import AuthService
from shop.src.services.OrderService import OrderService
from stripe import PaymentIntent


class CheckingControl:

    @staticmethod
    def checking(request, data) -> tuple[Payment, PaymentIntent] | HttpError:
        if not CheckInfos.is_positive_int(data.orderId):
            raise HttpError(400, "Invalid order id")
        if not CheckInfos.is_positive_int(data.paymentMethodId):
            raise HttpError(400, "Invalid payment method id")

        if not OrderService.is_cart(data.orderId):
            raise HttpError(400, "Order is not a cart")

        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)

        result, payment_intent, result_type = CheckingService.checking(
            user, data.orderId, data.paymentMethodId
        )

        if result:
            if payment_intent:
                if result_type == 0:
                    return {
                        "payment": result.to_json(),
                        "paymentIntent": payment_intent,
                    }
                elif result_type == 1:
                    return {
                        "subscription": result.to_json(),
                        "paymentIntent": payment_intent,
                    }
            else:
                if CheckingService.cancel(result.id, result_type):
                    raise HttpError(500, "Payment canceled")

        raise HttpError(500, "An error occurred while checking the payment")

from payments.models import Payment, Subscription
from payments.src.services.CheckingService import CheckingService
from utils.CheckInfos import CheckInfos
from ninja.errors import HttpError
from users.src.services.AuthService import AuthService
from shop.src.services.OrderService import OrderService
from stripe import PaymentIntent
from shop.src.services.OrderService import OrderService


class CheckingControl:

    @staticmethod
    def checking(request, data) -> tuple[Payment, PaymentIntent] | HttpError:
        if not CheckInfos.is_positive_int(data.orderId):
            raise HttpError(400, "Invalid order id")
        if not CheckInfos.is_positive_int(data.paymentMethodId):
            raise HttpError(400, "Invalid payment method id")

        if not OrderService.is_cart(data.orderId):
            raise HttpError(400, "Order is not a cart")

        order = OrderService.get_order_by_id(data.orderId)
        if order.billing_address is None:
            raise HttpError(400, "Billing address is not set")

        if order.recurrence == 0 or order.recurrence == 2:
            raise HttpError(400, "Recurrence type not implemented yet")

        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)

        result, payment_infos, result_type = CheckingService.checking(
            user, order, data.paymentMethodId
        )

        if result:
            if payment_infos:
                if result_type == 0:
                    return {
                        "payment": result.to_json(),
                        "paymentIntent": payment_infos,
                    }
                elif result_type == 1:
                    return {
                        "subscription": result.to_json(),
                        "clientSecret": payment_infos,
                    }
            else:
                if CheckingService.cancel(result.id, result_type):
                    raise HttpError(500, "Payment canceled")

        raise HttpError(500, "An error occurred while checking the payment")

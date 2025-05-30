from ninja.errors import HttpError
from payments.models import Payment
from payments.src.services.PaymentService import PaymentService
from users.src.services.AuthService import AuthService
from utils.CheckInfos import CheckInfos


class PaymentControl:

    @staticmethod
    def add(data) -> Payment | None:
        if not CheckInfos.is_positive_int(data.amount):
            raise HttpError(400, "Invalid amount")

        if data.orderId != None:
            if not CheckInfos.is_positive_int(data.orderId):
                raise HttpError(400, "Invalid order id")

        if data.subscriptionId != None:
            if not CheckInfos.is_positive_int(data.subscriptionId):
                raise HttpError(400, "Invalid subscription id")

        payment, payment_intent = PaymentService.add(
            data.amount,
            data.status,
            data.orderId,
            data.subscriptionId,
        )

        if payment.order != None and payment_intent is None:
            raise HttpError(500, "An error occurred while creating the payment")

        if payment:
            return {
                "payment": payment.to_json(),
                "paymentIntent": payment_intent,
            }
        else:
            raise HttpError(500, "An error occurred while creating the payment")

    @staticmethod
    def get(id: int) -> Payment | None:
        if not CheckInfos.is_positive_int(id):
            raise HttpError(400, "Invalid payment id")
        payment = PaymentService.get(id)
        if payment:
            return payment.to_json()
        else:
            raise HttpError(404, "Payment not found")

    @staticmethod
    def get_by_order(order_id: int) -> Payment | None:
        if not CheckInfos.is_positive_int(order_id):
            raise HttpError(400, "Invalid order id")
        payments = PaymentService.get_by_order(order_id)
        if payments:
            return [payment.to_json() for payment in payments]
        else:
            raise HttpError(404, "Payment not found")

    @staticmethod
    def get_all(request) -> list[Payment] | None:
        if not AuthService.isAdmin(request):
            raise HttpError(403, "Forbidden")
        payments = PaymentService.get_all()
        if payments:
            return [payment.to_json() for payment in payments]
        else:
            raise HttpError(404, "Payments not found")

    @staticmethod
    def get_all_by_subscription(subscription_id: int) -> list[Payment] | None:
        if not CheckInfos.is_positive_int(subscription_id):
            raise HttpError(400, "Invalid subscription id")
        payments = PaymentService.get_all_by_subscription(subscription_id)
        if payments:
            return [payment.to_json() for payment in payments]
        else:
            raise HttpError(404, "Payments not found")

    @staticmethod
    def update_status(data) -> Payment | None:
        if not CheckInfos.is_positive_int(data.id):
            raise HttpError(400, "Invalid payment id")
        if not CheckInfos.is_positive_int(data.status):
            raise HttpError(400, "Invalid status")
        payment = PaymentService.update_status(data.id, data.status)
        if payment:
            return payment.to_json()
        else:
            raise HttpError(500, "An error occurred while updating the payment")

    @staticmethod
    def delete(request, id: int) -> bool:
        if not AuthService.isAdmin(request):
            raise HttpError(403, "Forbidden")
        if not CheckInfos.is_positive_int(id):
            raise HttpError(400, "Invalid payment id")
        result = PaymentService.delete(id)
        if result:
            return True
        else:
            raise HttpError(500, "An error occurred while deleting the payment")

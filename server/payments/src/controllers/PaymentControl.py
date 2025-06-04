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
    def get_sales_metrics(request, params):
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(params.count):
                raise HttpError(400, "Invalid count")
            if params.period not in ("daily", "weekly"):
                raise HttpError(400, "Invalid period: must be 'weekly' or 'daily'")
        
            try:
                metrics = PaymentService.sales_metrics(params.period, params.count)

                if metrics:
                    return metrics
                else:
                    raise HttpError(404, "Metrics not found")
            except Exception as e:
                raise HttpError(500, f"Something went wrong while gettings sales metrics: {e}")
        else:
            raise HttpError(403, "Forbidden")
        
    @staticmethod
    def get_sales_metrics_by_category(request, params):
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(params.count):
                raise HttpError(400, "Invalid count")
            if params.period not in ("daily", "weekly"):
                raise HttpError(400, "Invalid period: must be 'weekly' or 'daily'")
            if not CheckInfos.is_valid_locale(params.locale):
                raise HttpError(400, "Invalid locale")
        
            try:
                metrics = PaymentService.sales_metrics_by_category(params.period, params.count, params.locale)

                if metrics:
                    return metrics
                else:
                    raise HttpError(404, "Metrics not found")
            except Exception as e:
                raise HttpError(500, f"Something went wrong while gettings sales by category metrics: {e}")
        else:
            raise HttpError(403, "Forbidden")

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
    def get_all_from_user(request):
        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)

        payments = PaymentService.get_all_from_user(user.id)
        if payments:
            return payments
        else:
            raise HttpError(404, f"Payments for user id '{user.id}' not found")

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

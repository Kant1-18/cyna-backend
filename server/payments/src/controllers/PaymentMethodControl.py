from payments.models import PaymentMethod
from payments.src.services.PaymentMethodService import PaymentMethodService
from users.src.services.AuthService import AuthService
from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos


class PaymentMethodControl:

    @staticmethod
    def add(request, data) -> PaymentMethod | None:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_string(data.name):
                raise HttpError(400, "Invalid string for name")

            if not CheckInfos.is_valid_string(data.stripeCode):
                raise HttpError(400, "Invalid string for stripe code")

            payment_method = PaymentMethodService.add(data.name, data.stripeCode)
            if payment_method:
                return payment_method.to_json()
            else:
                raise HttpError(
                    500, "An error occurred while creating the payment method"
                )
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def get(request, id: int) -> PaymentMethod | None:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(id):
                raise HttpError(400, "Invalid id")

            payment_method = PaymentMethodService.get(id)
            if payment_method:
                return payment_method.to_json()
            else:
                raise HttpError(404, "Payment method not found")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def get_all(request) -> list[PaymentMethod] | None:
        if AuthService.isAdmin(request):
            payment_methods = PaymentMethodService.get_all()
            if payment_methods:
                return [payment_method.to_json() for payment_method in payment_methods]
            else:
                raise HttpError(404, "No payment methods found")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def update(request, data) -> PaymentMethod | None:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data.id):
                raise HttpError(400, "Invalid id")

            if not CheckInfos.is_valid_string(data.name):
                raise HttpError(400, "Invalid string for name")

            if not CheckInfos.is_valid_string(data.stripeCode):
                raise HttpError(400, "Invalid string for stripe code")

            payment_method = PaymentMethodService.update(
                data.id, data.name, data.stripeCode
            )
            if payment_method:
                return payment_method.to_json()
            else:
                raise HttpError(
                    500, "An error occurred while updating the payment method"
                )
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def delete(request, id: int) -> bool:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(id):
                raise HttpError(400, "Invalid id")

            result = PaymentMethodService.delete(id)
            if result:
                return True
            else:
                raise HttpError(
                    500, "An error occurred while deleting the payment method"
                )
        else:
            raise HttpError(403, "Forbidden")

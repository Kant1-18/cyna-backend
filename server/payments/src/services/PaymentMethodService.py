from payments.models import PaymentMethod
from payments.src.data.repositories.PaymentMethodRepo import PaymentMethodRepo


class PaymentMethodService:

    @staticmethod
    def add(name: str, stripe_code: str) -> PaymentMethod | None:
        return PaymentMethodRepo.add(name, stripe_code)

    @staticmethod
    def get(id: int) -> PaymentMethod | None:
        return PaymentMethodRepo.get(id)

    @staticmethod
    def get_by_name(name: str) -> PaymentMethod | None:
        return PaymentMethodRepo.get_by_name(name)

    @staticmethod
    def update(method_id: int, name: str, stripe_code: str) -> PaymentMethod | None:
        return PaymentMethodRepo.update(method_id, name, stripe_code)

    @staticmethod
    def delete(method_id: int) -> bool:
        return PaymentMethodRepo.delete(method_id)

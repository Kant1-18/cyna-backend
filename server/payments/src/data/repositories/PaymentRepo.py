from payments.models import Payment, PaymentMethod, Subscription
from shop.models import Order


class PaymentRepo:
    @staticmethod
    def add(
        payment_method: PaymentMethod,
        amount: int,
        status: int = 0,
        order: Order = None,
        subscription: Subscription = None,
    ) -> Payment | None:
        try:
            payment = Payment.objects.create(
                payment_method=payment_method,
                amount=amount,
                status=status,
                order=order,
                subscription=subscription,
            )
            if payment:
                return payment
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get(id: int) -> Payment | None:
        try:
            payment = Payment.objects.get(id=id)
            if payment:
                return payment
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_order(order: Order) -> list[Payment] | None:
        try:
            payments = Payment.objects.filter(order=order)
            if payments:
                return payments
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> list[Payment] | None:
        try:
            payments = Payment.objects.all()
            if payments:
                return payments
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_by_subscription(subscription: Subscription) -> list[Payment] | None:
        try:
            payments = Payment.objects.filter(subscription=subscription)
            if payments:
                return payments
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_status(payment: Payment, status: int) -> Payment | None:
        try:
            payment.status = status
            payment.save()
            return payment
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete(payment: Payment) -> bool:
        try:
            payment.delete()
            return True
        except Exception as e:
            print(e)

        return False

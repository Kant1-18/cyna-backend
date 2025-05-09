from payments.models import Payment, PaymentMethod, Subscription
from shop.models import Order
from payments.src.data.repositories.PaymentRepo import PaymentRepo
from shop.src.services.OrderService import OrderService
from payments.src.services.PaymentMethodService import PaymentMethodService
from payments.src.services import SubscriptionService
import utils.sendInvoice as sendInvoice


class PaymentService:
    @staticmethod
    def add(
        payment_method_id: int,
        amount: int,
        status: int = 0,
        order_id: int = None,
        subscription_id: int = None,
    ) -> Payment | None:
        try:
            payment_method = PaymentMethodService.get(payment_method_id)
            if payment_method:
                order = OrderService.get_order_by_id(order_id) if order_id else None
                subscription = (
                    SubscriptionService.get(subscription_id)
                    if subscription_id
                    else None
                )
                return PaymentRepo.add(
                    payment_method=payment_method,
                    amount=amount,
                    status=status,
                    order=order,
                    subscription=subscription,
                )
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get(id: int) -> Payment | None:
        try:
            payment = PaymentRepo.get(id)
            if payment:
                return payment
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_order(order_id: int) -> list[Payment] | None:
        try:
            order = OrderService.get_order_by_id(order_id)
            payment = PaymentRepo.get_by_order(order)
            if payment:
                return payment
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> list[Payment] | None:
        try:
            payments = PaymentRepo.get_all()
            if payments:
                return payments
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_by_subscription(subscription_id: int) -> list[Payment] | None:
        try:
            subscription = SubscriptionService.get(subscription_id)
            payments = PaymentRepo.get_all_by_subscription(subscription)
            if payments:
                return payments
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_status(payment_id: int, status: int) -> Payment | None:
        try:
            payment = PaymentRepo.get(payment_id)
            if payment:
                payment = PaymentRepo.update_status(payment, status)
                if status == 5:
                    if payment.order != None and payment.subscription == None:
                        sendInvoice.send_order_invoice(
                            payment.order.user.email,
                            payment.order,
                        )
                    elif payment.subscription != None and payment.order == None:
                        sendInvoice.send_subscription_invoice(
                            payment.subscription.user.email,
                            payment.subscription,
                        )
                return payment
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete(payment_id: int) -> bool:
        try:
            payment = PaymentRepo.get(payment_id)
            if payment:
                if PaymentRepo.delete(payment):
                    return True
        except Exception as e:
            print(e)

        return False

from typing import Dict, List
from payments.models import Payment, PaymentMethod, Subscription
from shop.models import Order
from payments.src.data.repositories.PaymentRepo import PaymentRepo
from shop.src.services.OrderService import OrderService
from payments.src.services.PaymentMethodService import PaymentMethodService
from payments.src.services import SubscriptionService
import utils.emails as sendInvoice
from utils.Stripe import PaymentIntent


class PaymentService:
    @staticmethod
    def add(
        amount: int,
        status: int = 0,
        order_id: int = None,
        subscription_id: int = None,
    ) -> tuple[Payment, PaymentIntent] | None:
        from utils.Stripe import StripeUtils

        try:
            order = OrderService.get_order_by_id(order_id) if order_id else None
            subscription = (
                SubscriptionService.get(subscription_id) if subscription_id else None
            )

            payment = PaymentRepo.add(
                amount=amount,
                status=status,
                order=order,
                subscription=subscription,
            )

            if order is not None:
                payment_intent = StripeUtils.create_payment_intent(
                    amount=amount,
                    user_stripe_id=order.user.stripe_id,
                )

                return payment, payment_intent
            else:
                return payment, None

        except Exception as e:
            print(e)

        return None

    @staticmethod
    def sales_metrics(period: str, count: int):
        try:
            metrics = PaymentRepo.get_sales_metrics(period, count)
            if metrics:
                return metrics
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def sales_metrics_by_category(period: str, count: int, locale: str):
        try:
            metrics = PaymentRepo.get_sales_by_category(period, count, locale)
            if metrics:
                return metrics
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
    def get_pending_subscription(subscription: Subscription) -> Payment | None:
        try:
            payment = PaymentRepo.get_pending_subscription(subscription)
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
    def get_all_from_user(user_id: int) -> List[Dict]:
        try:
            payments = PaymentRepo.get_all_from_user(user_id)
            if payments:
                return [payment.to_json() for payment in payments]
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
                if status == 4:
                    if payment.order != None and payment.subscription == None:
                        sendInvoice.send_order_invoice(
                            payment.order.user.email,
                            payment.order,
                        )
                    elif payment.subscription != None and payment.order != None:
                        payment.order
                        sendInvoice.send_receipt(
                            payment.subscription.user.email,
                            payment.subscription,
                        )
                return payment
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_invoice(payment_id: int, invoice_url: str) -> Payment | None:
        try:
            payment = PaymentRepo.get(payment_id)
            if payment:
                updated_payment = PaymentRepo.update_incoice(payment, invoice_url)
                if updated_payment:
                    return updated_payment
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

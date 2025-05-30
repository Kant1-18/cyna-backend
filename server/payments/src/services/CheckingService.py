from payments.models import Subscription, PaymentMethod, Payment
from payments.src.services.SubscriptionService import SubscriptionService
from payments.src.services.PaymentService import PaymentService
from shop.models import Order, OrderItem, Product
from shop.src.services.OrderService import OrderService
from users.models import User
from stripe import PaymentIntent


class CheckingService:

    @staticmethod
    def checking(
        user: User, order: Order
    ) -> tuple[Subscription | Payment, PaymentIntent, int] | tuple[None, None, None]:
        try:
            if order.recurrence == 0:
                return CheckingService.payment_checking(user, order)
            else:
                return CheckingService.subscription_checking(user, order)
        except Exception as e:
            print(e)
            return None, None, None

    @staticmethod
    def payment_checking(
        user: User, order: Order
    ) -> tuple[Payment, PaymentIntent] | None:
        try:
            order_items = OrderService.get_all_items(order)
            amount = sum([item.quantity * item.product.price for item in order_items])

            payment, payment_intent = PaymentService.add(
                amount=amount,
                status=0,
                order_id=order.id,
            )

            if payment and payment_intent:
                return payment, payment_intent, 0

        except Exception as e:
            print(e)
            return None, None, None

    @staticmethod
    def subscription_checking(
        user: User, order: Order
    ) -> tuple[Subscription, PaymentIntent] | None:
        try:
            subsciption, client_secret = SubscriptionService.add(
                user_id=user.id,
                billing_address_id=order.billing_address.id,
                recurrence=order.recurrence,
                order_id=order.id,
            )

            if subsciption and client_secret:
                return subsciption, client_secret, 1

        except Exception as e:
            print(e)
            return None, None, None

    @staticmethod
    def cancel(result_id: int, result_type: int) -> bool:
        try:
            if result_type == 0:
                return PaymentService.delete(result_id)
            elif result_type == 1:
                return SubscriptionService.delete_subscription(result_id)
        except Exception as e:
            print(e)
            return None

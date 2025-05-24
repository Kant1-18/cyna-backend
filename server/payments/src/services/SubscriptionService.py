from payments.models import Subscription, SubscriptionItem, PaymentMethod
from users.models import User, Address
from shop.models import Order, OrderItem, Product
from payments.src.data.repositories.SubscriptionRepo import SubscriptionRepo
from payments.src.data.repositories.SubscriptionItemRepo import SubscriptionItemRepo
from payments.src.data.repositories.PaymentMethodRepo import PaymentMethodRepo
from users.src.services.UserService import UserService
from users.src.services.AddressService import AddressService
from utils.Stripe import StripeUtils
from shop.src.services.OrderService import OrderService
from shop.src.data.repositories.OrderItemRepo import OrderItemRepo
from stripe import PaymentIntent


class SubscriptionService:

    @staticmethod
    def add(
        user_id: int,
        billing_address_id: int,
        recurrence: int,
        order_id: int,
    ) -> tuple[Subscription, PaymentIntent] | None:
        try:
            user = UserService.get(user_id)
            address = AddressService.get(billing_address_id)

            order = OrderService.get_order_by_id(order_id)
            OrderService.update_order_status(order_id, 1)

            if SubscriptionRepo.have_active_subscription(user):
                subscription = SubscriptionRepo.get_by_user(user)
                return SubscriptionService.add_order_in_subscription(
                    subscription,
                    order,
                )

            stripe_subscription, client_secret = StripeUtils.create_subscription(
                customer_id=user.stripe_id,
                recurrence=recurrence,
                order=order,
            )

            if stripe_subscription:
                subscription = SubscriptionRepo.add(
                    user=user,
                    status=0,
                    billing_address=address,
                    stripe_id=stripe_subscription.id,
                    recurrence=order.recurrence,
                )

                if subscription:
                    for item in order.items.all():
                        subscription_item = SubscriptionItemRepo.add(
                            subscription=subscription,
                            order_item=item,
                        )
                        if not subscription_item:
                            OrderService.update_order_status(order_id, 2)
                            return None

                    return subscription, client_secret

        except Exception as e:
            OrderService.update_order_status(order_id, 2)
            print(e)

        return None, None

    @staticmethod
    def add_order_in_subscription(subscription: Subscription, order: Order) -> bool:
        try:
            OrderService.update_order_status(order.id, 1)

            recurrence = subscription.recurrence
            for item in order.items.all():
                for i in range(item.quantity):
                    if StripeUtils.add_item_subscription(
                        subscription_id=subscription.stripe_id,
                        product_id=(
                            item.product.stripe_monthly_price_id
                            if recurrence == 0
                            else item.product.stripe_yearly_price_id
                        ),
                    ):
                        continue
                    else:
                        return None

                subscription_item = SubscriptionItemRepo.add(
                    subscription_id=subscription.id,
                    order_item=item,
                )

                if subscription_item:
                    continue
                else:
                    return None
            return subscription
        except Exception as e:
            OrderService.update_order_status(order.id, 2)
            print(e)

        return None

    @staticmethod
    def get_subscription_by_id(subscription_id: int) -> Subscription | None:
        try:
            subscription = SubscriptionRepo.get(subscription_id)
            if subscription:
                return subscription
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_subscription_by_user(user_id: int) -> Subscription | None:
        try:
            user = UserService.get(user_id)
            subscriptions = SubscriptionRepo.get_by_user(user)
            if subscriptions:
                return subscriptions
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_address(
        subscription_id: int, billing_address_id: int
    ) -> Subscription | None:
        try:
            subscription = SubscriptionRepo.get(subscription_id)
            if subscription:
                address = AddressService.get(billing_address_id)
                if address:
                    return SubscriptionRepo.update_address(subscription_id, address)
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def update_status(subscription_id: int, status: int) -> Subscription | None:
        try:
            subscription = SubscriptionRepo.get(subscription_id)
            if subscription:
                return SubscriptionRepo.update_status(subscription_id, status)
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def update_recurrence(subscription_id: int, recurrence: int) -> Subscription | None:
        try:
            subscription = SubscriptionRepo.get(subscription_id)
            if subscription:
                return SubscriptionRepo.update_recurrence(subscription_id, recurrence)
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def delete_item_subscription(subscription_id: int, order_item_id: int) -> bool:
        try:
            subscription = SubscriptionRepo.get(subscription_id)
            if subscription:
                order_item = OrderItemRepo.get_by_id(order_item_id)
                if order_item:
                    if StripeUtils.delete_item_subscription(
                        subscription_id=subscription.stripe_id,
                        product_id=(
                            order_item.product.stripe_monthly_price_id
                            if subscription.recurrence == 0
                            else order_item.product.stripe_yearly_price_id
                        ),
                    ):
                        SubscriptionRepo.delete_item_subscription(
                            subscription_id, order_item_id
                        )
                        return True
        except Exception as e:
            print(e)

        return False

    @staticmethod
    def delete_subscription(subscription_id: int) -> bool:
        try:
            subscription = SubscriptionRepo.get(subscription_id)
            if subscription:
                if StripeUtils.delete_subscription(
                    subscription_id=subscription.stripe_id
                ):
                    SubscriptionRepo.delete(subscription_id)
                    return True
        except Exception as e:
            print(e)

        return False

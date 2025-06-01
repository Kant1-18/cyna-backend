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
from stripe import PaymentIntent, stripe
from ninja.errors import HttpError


class SubscriptionService:

    @staticmethod
    def add(
        user_id: int,
        billing_address_id: int,
        payment_method_id: int,
        recurrence: int,
        order_id: int,
    ) -> tuple[Subscription, PaymentIntent] | None:
        try:
            user = UserService.get(user_id)
            address = AddressService.get(billing_address_id)
            payment_method = PaymentMethodRepo.get(payment_method_id)

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
                    payment_method=payment_method,
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
    def cancel_subscription(subscription: Subscription, stripe_subscription_item_id: str, user: User):
        stripe_sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id, expand=["items"])
        stripe_items = stripe_sub["items"]["data"]

        if len(stripe_items) > 1:
            try:
                cancelled_item = stripe.SubscriptionItem.delete(stripe_subscription_item_id, proration_behavior="none")
            except stripe.error.StripeError as e:
                raise HttpError(400, f"Stripe error: {e.user_message}")
            
            SubscriptionItemRepo.delete_by_stripe_item_id(stripe_subscription_item_id)
        
        else :
            try: 
                cancelled_sub = stripe.Subscription.cancel(subscription.stripe_subscription_id, prorate=False)
            except stripe.error.StripeError as e:
                raise HttpError(400, f"Stripe error: {e.user_message}")
        
            SubscriptionItemRepo.delete_by_subscription_id(subscription.id)
            SubscriptionRepo.update_status(subscription.id, "canceled")

        return SubscriptionService.get_subscription_by_user(user, "all")


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
    def get_subscription_by_user(user: User, status) -> Subscription | None:
        try:
            if status is None or status.lower() == "all":
                local_subscriptions = SubscriptionRepo.get_by_user(user.id, status=None)
            else:
                local_subscriptions = SubscriptionRepo.get_by_user(user.id, status=status.lower())

            if not local_subscriptions:
                return []
            
            result = []
            for local_subscription in local_subscriptions:
                result.append(local_subscription.to_json())
            
            return result
            
        except Exception as e:
            print(f"[SubscriptionService.get_subscription_by_user] error: {e}")
            raise HttpError(500, "Failed to fetch subscriptions")

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
    def update_status(subscription_id: int, status: int, user: User) -> Subscription | None:
        try:
            subscription = SubscriptionRepo.get(subscription_id)
            if subscription:
                SubscriptionRepo.update_status(subscription_id, status)
                updated_subscriptions = SubscriptionService.get_subscription_by_user(user, "active")
                return updated_subscriptions
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

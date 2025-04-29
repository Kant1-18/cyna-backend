from payments.models import Subscription, SubscriptionItem, PaymentMethod
from users.models import User, Address
from shop.models import Order, OrderItem, Product
from payments.src.data.repositories.SubscriptionRepo import SubscriptionRepo
from payments.src.data.repositories.SubscriptionItemRepo import SubscriptionItemRepo
from payments.src.data.repositories.PaymentMethodRepo import PaymentMethodRepo
from users.src.services.UserService import UserService
from users.src.services.AddressService import AddressService
from utils.Stripe import Stripe
from shop.src.services.OrderService import OrderService


class SubscriptionService:

    @staticmethod
    def add(
        user_id: int,
        billing_address_id: int,
        payment_method_id: int,
        recurrence: bool,
        order_id: int,
    ):
        try:
            user = UserService.get(user_id)
            address = AddressService.get(billing_address_id)
            payment_method = PaymentMethodRepo.get(payment_method_id)

            order = OrderService.get(order_id)

            stripe_subscription = Stripe.create_subscription(
                customer_id=user.stripe_id,
                recurrence=recurrence,
                order=order,
            )

            if stripe_subscription:
                subscription = SubscriptionRepo.add(
                    user_id=user.id,
                    billing_address_id=address.id,
                    payment_method_id=payment_method.id,
                    stripe_id=stripe_subscription.id,
                    recurrence=recurrence,
                )

                if subscription:
                    for item in order.items.all():
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
            print(e)

        return None

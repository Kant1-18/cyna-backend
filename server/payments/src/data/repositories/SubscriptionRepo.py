from payments.models import Subscription, PaymentMethod
from users.models import User, Address


class SubscriptionRepo:

    @staticmethod
    def add(
        user: User,
        status: int,
        billing_address: Address,
        stripe_id: str,
        payment_method: PaymentMethod,
        recurrence: bool,
    ) -> Subscription | None:
        try:
            subscription = Subscription.objects.create(
                user=user,
                status=status,
                billing_address=billing_address,
                payment_method=payment_method,
                stripe_id=stripe_id,
                recurrence=recurrence,
            )
            if subscription:
                return subscription
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get(id: int) -> Subscription | None:
        try:
            subscription = Subscription.objects.get(id=id)
            if subscription:
                return subscription
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_user(user: User) -> Subscription | None:
        try:
            subscription = Subscription.objects.get(user=user)
            if subscription:
                return subscription
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> list[Subscription] | None:
        try:
            subscriptions = Subscription.objects.all()
            if subscriptions:
                return subscriptions
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_address(id: int, billing_address: Address) -> Subscription | None:
        try:
            subscription = Subscription.objects.get(id=id)
            if subscription:
                subscription.billing_address = billing_address
                subscription.save()
                return subscription
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_status(id: int, status: int) -> Subscription | None:
        try:
            subscription = Subscription.objects.get(id=id)
            if subscription:
                subscription.status = status
                subscription.save()
                return subscription
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete(id: int) -> bool:
        try:
            subscription = Subscription.objects.get(id=id)
            if subscription:
                subscription.delete()
                return True
        except Exception as e:
            print(e)

        return False

    @staticmethod
    def have_subscription(user: User) -> bool:
        try:
            return Subscription.objects.filter(user=user).exists()
        except Exception as e:
            print(e)

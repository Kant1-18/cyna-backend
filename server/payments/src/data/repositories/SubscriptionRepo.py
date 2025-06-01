from payments.models import Subscription, PaymentMethod
from users.models import User, Address
from django.db.models import QuerySet
from django.utils import timezone


class SubscriptionRepo:

    @staticmethod
    def add(
        user: User,
        status: str,
        billing_address: Address,
        payment_method: PaymentMethod,
        stripe_subscription_id: str,
        recurrence: int,
        default_payment_method_id: str,
        order_id: int,
    ) -> Subscription | None:
        try:
            subscription = Subscription.objects.create(
                user=user,
                status=status,
                billing_address=billing_address,
                payment_method=payment_method,
                stripe_subscription_id=stripe_subscription_id,
                recurrence=recurrence,
                default_payment_method_id=default_payment_method_id,
                order_id=order_id,
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

    # quick fix : review code
    @staticmethod
    def get_by_user(user_id: int, status: str | None) -> QuerySet[Subscription] | None:
        try:
            subscriptions = Subscription.objects.filter(user=user_id, **({} if status is None else {"status": status}))

            if subscriptions:
                return subscriptions
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
    def update_status(id: int, status: str, last_invoice_url: str = None) -> Subscription | None:
        try:
            subscription = Subscription.objects.get(id=id)
            if subscription:
                subscription.status = status
                subscription.updated_at = timezone.now()
                if last_invoice_url is not None:
                    subscription.last_invoice_url = last_invoice_url
                subscription.save()
                return subscription
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def update_by_stripe_id(id: str, status: str, last_invoice_url: str = None) -> Subscription | None:
        try:
            subscription = Subscription.objects.filter(stripe_subscription_id=id).first()
            if subscription:
                subscription.status = status
                subscription.updated_at = timezone.now()
                if last_invoice_url is not None:
                    subscription.last_invoice_url = last_invoice_url
                subscription.save()
                return subscription
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_recurrence(id: int, recurrence: int) -> Subscription | None:
        try:
            subscription = Subscription.objects.get(id=id)
            if subscription:
                subscription.recurrence = recurrence
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
    def have_active_subscription(user: User) -> bool:
        try:
            subscription = Subscription.objects.filter(user=user, status=1)
            if subscription:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return None

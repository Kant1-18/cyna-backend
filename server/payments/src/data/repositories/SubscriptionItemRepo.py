from payments.models import SubscriptionItem, Subscription
from shop.models import OrderItem


class SubscriptionItemRepo:

    @staticmethod
    def add(
        subscription: Subscription, order_item: OrderItem
    ) -> SubscriptionItem | None:
        try:
            subscription_item = SubscriptionItem.objects.create(
                subscription=subscription, order_item=order_item
            )
            if subscription_item:
                return subscription_item
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def get(id: int) -> SubscriptionItem | None:
        try:
            subscription_item = SubscriptionItem.objects.get(id=id)
            if subscription_item:
                return subscription_item
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def get_all_by_subscription(
        subscription: Subscription,
    ) -> list[SubscriptionItem] | None:
        try:
            subscription_items = SubscriptionItem.objects.filter(
                subscription=subscription
            )
            if subscription_items:
                return subscription_items
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def delete(subscription_item: SubscriptionItem) -> bool:
        try:
            subscription_item.delete()
            return True
        except Exception as e:
            print(e)
        return False

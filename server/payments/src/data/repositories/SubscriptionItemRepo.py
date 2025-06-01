from payments.models import SubscriptionItem, Subscription
from shop.models import OrderItem
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils import timezone


class SubscriptionItemRepo:

    @staticmethod
    def add(
        subscription: Subscription, 
        order_item: OrderItem, 
        stripe_item_id: str, 
        current_period_start: datetime,
        current_period_end: datetime,
        price_id: str, 
        quantity: int
    ) -> SubscriptionItem | None:
        try:
            subscription_item = SubscriptionItem.objects.create(
                subscription=subscription,
                order_item=order_item,
                stripe_item_id=stripe_item_id,
                current_period_start=current_period_start,
                current_period_end=current_period_end,
                price_id=price_id,
                quantity=quantity
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
    def update_periods_by_stripe_id(stripe_item_id: str, new_start: timezone, new_end: timezone) -> SubscriptionItem:
        try:
            subscription_item: SubscriptionItem = SubscriptionItem.objects.get(stripe_item_id=stripe_item_id)

            if subscription_item:
                subscription_item.current_period_start = timezone.datetime.fromtimestamp(new_start, tz=timezone.get_current_timezone())
                subscription_item.current_period_end = timezone.datetime.fromtimestamp(new_end, tz=timezone.get_current_timezone())
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
    
    @staticmethod
    def delete_by_stripe_item_id(stripe_item_id: str):
        try:
            item = SubscriptionItem.objects.get(stripe_item_id=stripe_item_id)
            item.delete()
            return True
        except ObjectDoesNotExist:
            return False
        except Exception as e:
            print(e)
            return False
        
    @staticmethod
    def delete_by_subscription_id(subscription_id: int) -> int:
        try:
            deleted, _ = SubscriptionItem.objects.filter(
                subscription_id=subscription_id
            ).delete()
            return deleted
        except Exception as e:
            print(f"[SubscriptionItemRepo.delete_all_for_subscription] {e}")
            return 0
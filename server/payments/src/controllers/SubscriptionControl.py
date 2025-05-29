from ninja.errors import HttpError
from payments.models import Subscription
from payments.src.services.SubscriptionService import SubscriptionService
from users.src.services.AuthService import AuthService
from utils.CheckInfos import CheckInfos


class SubscriptionControl:

    @staticmethod
    def add(request, data) -> Subscription | None:
        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)

        if not CheckInfos.is_positive_int(data.billingAddressId):
            raise HttpError(400, "Invalid billing address id")
        if not CheckInfos.is_positive_int(data.paymentMethodId):
            raise HttpError(400, "Invalid payment method id")
        if not CheckInfos.is_positive_int(data.orderId):
            raise HttpError(400, "Invalid order id")
        if not CheckInfos.is_positive_int(data.recurrence):
            raise HttpError(400, "Invalid recurrence")

        subscription, client_secret = SubscriptionService.add(
            user.id,
            data.billingAddressId,
            data.paymentMethodId,
            data.recurrence,
            data.orderId,
        )

        if subscription:
            return {
                "subscription": subscription.to_json(),
                "clientSecret": client_secret,
            }
        else:
            raise HttpError(500, "An error occurred while creating the subscription")

    @staticmethod
    def get_by_user(request, user_id: int) -> Subscription | None:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(user_id):
                raise HttpError(400, "Invalid user id")

            subscription = SubscriptionService.get_subscription_by_user(user_id)
            if subscription:
                return subscription.to_json()
            else:
                raise HttpError(404, "Subscription not found")
        else:
            raise HttpError(403, "Forbidden")

    # quick fix : review code
    @staticmethod
    def get_my(request) -> Subscription | None:
        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)

        subscriptions = SubscriptionService.get_subscription_by_user(user.id)

        if subscriptions:
            return [subscription.to_json() for subscription in subscriptions]
        else:
            raise HttpError(404, "Subscription not found")

    @staticmethod
    def get_all(request) -> list[Subscription] | None:
        if AuthService.isAdmin(request):
            subscriptions = SubscriptionService.get_all()

            if subscriptions:
                return [subscription.to_json() for subscription in subscriptions]
            else:
                raise HttpError(404, "No subscriptions found")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def update_billing_address(data) -> Subscription | None:
        if not CheckInfos.is_positive_int(data.id):
            raise HttpError(400, "Invalid subscription id")
        if not CheckInfos.is_positive_int(data.billingAddressId):
            raise HttpError(400, "Invalid billing address id")

        subscription = SubscriptionService.update_address(
            data.id,
            data.billingAddressId,
        )

        if subscription:
            return subscription.to_json()
        else:
            raise HttpError(500, "An error occurred while updating the subscription")

    @staticmethod
    def update_status(data) -> Subscription | None:
        if not CheckInfos.is_positive_int(data.id):
            raise HttpError(400, "Invalid subscription id")
        if not CheckInfos.is_positive_int(data.status):
            raise HttpError(400, "Invalid status")

        subscription = SubscriptionService.update_status(
            data.id,
            data.status,
        )

        if subscription:
            return subscription.to_json()
        else:
            raise HttpError(500, "An error occurred while updating the subscription")

    @staticmethod
    def update_recurrence(data) -> Subscription | None:
        if not CheckInfos.is_positive_int(data.id):
            raise HttpError(400, "Invalid subscription id")
        if not CheckInfos.is_positive_int(data.recurrence):
            raise HttpError(400, "Invalid recurrence")

        subscription = SubscriptionService.update_recurrence(
            data.id,
            data.recurrence,
        )

        if subscription:
            return subscription.to_json()
        else:
            raise HttpError(500, "An error occurred while updating the subscription")

    @staticmethod
    def delete_item(data) -> bool:
        if not CheckInfos.is_positive_int(data.id):
            raise HttpError(400, "Invalid subscription id")
        if not CheckInfos.is_positive_int(data.orderItemId):
            raise HttpError(400, "Invalid order item id")

        result = SubscriptionService.delete_item_subscription(
            data.id,
            data.orderItemId,
        )

        if result:
            return True
        else:
            raise HttpError(
                500, "An error occurred while deleting the subscription item"
            )

    @staticmethod
    def delete(request, id: int) -> bool:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(id):
                raise HttpError(400, "Invalid subscription id")

            result = SubscriptionService.delete_subscription(id)

            if result:
                return True
            else:
                raise HttpError(
                    500, "An error occurred while deleting the subscription"
                )
        else:
            raise HttpError(403, "Forbidden")

from datetime import datetime
import stripe.error
from payments.models import Payment, Subscription
from payments.src.services.CheckingService import CheckingService
from utils.CheckInfos import CheckInfos
from ninja.errors import HttpError
from users.src.services.AuthService import AuthService
from shop.src.services.OrderService import OrderService
from stripe import PaymentIntent, stripe
from shop.src.services.OrderService import OrderService
from payments.src.services.PaymentMethodService import PaymentMethodService
from payments.src.data.repositories.PaymentRepo import PaymentRepo
from payments.src.data.repositories.SubscriptionRepo import SubscriptionRepo
from payments.src.data.repositories.SubscriptionItemRepo import SubscriptionItemRepo
from shop.src.data.repositories.OrderItemRepo import OrderItemRepo
from django.utils import timezone


class CheckingControl:
    # Review and split code
    @staticmethod
    def checking(request, data) -> dict | HttpError:
        if not CheckInfos.is_positive_int(data.orderId):
            raise HttpError(400, "Invalid order id")
        if not OrderService.is_cart(data.orderId):
            raise HttpError(400, "Order is not a cart")
        order = OrderService.get_order_by_id(data.orderId)
        if order.billing_address is None:
            raise HttpError(400, "Billing address is not set")
        if order.shipping_address is None:
            raise HttpError(400, "Shipping address is not set")

        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)
        customer_id = user.stripe_id
        # add user verif

        payment_method = PaymentMethodService.get_by_name(data.paymentMethodType)

        items = OrderService.get_all_items(order)
        one_time = [item for item in items if item.recurring == 0]
        monthly = [item for item in items if item.recurring == 1]
        yearly = [item for item in items if item.recurring == 2]

        payments: list[dict] = []

        if one_time:
            amount = sum(item.product.price * item.quantity for item in one_time)
            try:
                stripe_intent = stripe.PaymentIntent.create(
                    customer=customer_id,
                    amount=amount,
                    currency="eur",
                    payment_method=data.paymentMethodId,
                    confirm=True,
                    metadata={"order_id": str(order.id)}
                )
            except stripe.error.StripeError as e:
                raise HttpError(400, f"One-time payment error: {e.user_message}")
            payment = PaymentRepo.add(
                payment_method=payment_method,
                amount=amount,
                status=0,
                order=order,
                subscription=None
            )
            payments.append({
                "type": "one_time",
                "id": stripe_intent.id,
                "clientSecret": stripe_intent.client_secret,
            })

        if monthly:
            monthly_items = [{"price": item.product.stripe_monthly_price_id, "quantity": item.quantity, "metadata": {"order_item_id": item.id}} for item in monthly]
            try:
                stripe_subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=monthly_items,
                    default_payment_method=data.paymentMethodId,
                    payment_behavior="default_incomplete",
                    payment_settings={"save_default_payment_method": "on_subscription"},
                    expand=["latest_invoice.confirmation_secret"],
                    metadata={"order_id": str(order.id)}
                )
            except stripe.error.StripeError as e:
                raise HttpError(400, f"Monthly subscription error: {e.user_message}")
            client_secret = stripe_subscription.latest_invoice.confirmation_secret.client_secret
            local_subscription = SubscriptionRepo.add(
                user=user,
                stripe_subscription_id=stripe_subscription.id,
                status=stripe_subscription.status,
                order_id=int(stripe_subscription.metadata.get("order_id", 0)),
                default_payment_method_id=stripe_subscription.default_payment_method,
                recurrence=1,
                billing_address=order.billing_address,
                payment_method=payment_method,
            )
            payment = PaymentRepo.add(
                payment_method=payment_method,
                amount=sum(item.product.price * item.quantity for item in monthly),
                status=0,
                order=order,
                subscription=local_subscription
            )
            if local_subscription:
                stripe_items = stripe_subscription.get("items", {}).get("data", [])
                for stripe_item in stripe_items:
                    metadata_id = int(stripe_item.metadata.order_item_id)
                    order_item = OrderItemRepo.get_by_id(metadata_id);
                    sub_item = SubscriptionItemRepo.add(
                        subscription=local_subscription, 
                        order_item=order_item, 
                        stripe_item_id=stripe_item.id,
                        current_period_start=timezone.datetime.fromtimestamp(stripe_item.current_period_start, tz=timezone.get_current_timezone()),
                        current_period_end=timezone.datetime.fromtimestamp(stripe_item.current_period_end, tz=timezone.get_current_timezone()),
                        price_id=stripe_item.price.id,
                        quantity=stripe_item.quantity,
                    )
                    if not sub_item:
                        OrderService.update_order_status(order.id, 2)
            payments.append({
                "type": "monthly",
                "stripe_id": stripe_subscription.id,
                "id": local_subscription.id,
                "clientSecret": client_secret,
            })

        if yearly:
            yearly_items = [{"price": item.product.stripe_yearly_price_id, "quantity": item.quantity, "metadata": {"order_item_id": item.id}} for item in yearly]
            try:
                stripe_subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=yearly_items,
                    default_payment_method=data.paymentMethodId,
                    payment_behavior="default_incomplete",
                    payment_settings={"save_default_payment_method": "on_subscription"},
                    expand=["latest_invoice.confirmation_secret"],
                    metadata={"order_id": str(order.id)}
                )
            except stripe.error.StripeError as e:
                raise HttpError(400, f"Yearly subscription error: {e.user_message}")
            client_secret = stripe_subscription.latest_invoice.confirmation_secret.client_secret
            local_subscription = SubscriptionRepo.add(
                user=user,
                stripe_subscription_id=stripe_subscription.id,
                status=stripe_subscription.status,
                order_id=int(stripe_subscription.metadata.get("order_id", 0)),
                default_payment_method_id=stripe_subscription.default_payment_method,
                recurrence=2,
                billing_address=order.billing_address,
                payment_method=payment_method,
            )
            payment = PaymentRepo.add(
                payment_method=payment_method,
                amount=sum(item.product.price * item.quantity for item in yearly),
                status=0,
                order=order,
                subscription=local_subscription
            )
            if local_subscription:
                stripe_items = stripe_subscription.get("items", {}).get("data", [])
                for stripe_item in stripe_items:
                    metadata_id = int(stripe_item.metadata.order_item_id)
                    order_item = OrderItemRepo.get_by_id(metadata_id);
                    sub_item = SubscriptionItemRepo.add(
                        subscription=local_subscription, 
                        order_item=order_item, 
                        stripe_item_id=stripe_item.id,
                        current_period_start=timezone.datetime.fromtimestamp(stripe_item.current_period_start, tz=timezone.get_current_timezone()),
                        current_period_end=timezone.datetime.fromtimestamp(stripe_item.current_period_end, tz=timezone.get_current_timezone()),
                        price_id=stripe_item.price.id,
                        quantity=stripe_item.quantity,
                    )
                    if not sub_item:
                        OrderService.update_order_status(order.id, 2)
            payments.append({
                "type": "yearly",
                "stripe_id": stripe_subscription.id,
                "id": local_subscription.id,
                "clientSecret": client_secret,
            })

        if not payments:
            raise HttpError(400, "No payable items in this order")

        return {"payments": payments}
    
    # Old method
    @staticmethod
    def _checking(request, data) -> tuple[Payment, PaymentIntent] | HttpError:
        if not CheckInfos.is_positive_int(data.orderId):
            raise HttpError(400, "Invalid order id")
        if not CheckInfos.is_positive_int(data.paymentMethodId):
            raise HttpError(400, "Invalid payment method id")

        if not OrderService.is_cart(data.orderId):
            raise HttpError(400, "Order is not a cart")

        order = OrderService.get_order_by_id(data.orderId)
        if order.billing_address is None:
            raise HttpError(400, "Billing address is not set")

        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)

        result, payment_infos, result_type = CheckingService.checking(
            user, order, data.paymentMethodId
        )

        if result:
            if payment_infos:
                if result_type == 0:
                    return {
                        "payment": result.to_json(),
                        "paymentIntent": payment_infos,
                    }
                elif result_type == 1:
                    return {
                        "subscription": result.to_json(),
                        "clientSecret": payment_infos,
                    }
            else:
                if CheckingService.cancel(result.id, result_type):
                    raise HttpError(500, "Payment canceled")

        raise HttpError(500, "An error occurred while checking the payment")

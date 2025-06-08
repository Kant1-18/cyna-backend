from payments.src.services.PaymentService import PaymentService
from shop.models import Order
from shop.src.services.OrderService import OrderService
from users.models import User
from payments.src.data.repositories.SubscriptionItemRepo import SubscriptionItemRepo
from payments.src.data.repositories.SubscriptionRepo import SubscriptionRepo
from payments.src.data.repositories.PaymentRepo import PaymentRepo
from ninja.errors import HttpError
from payments.src.services.PaymentMethodService import PaymentMethodService
from django.utils import timezone
from utils.Stripe import stripe
from shop.src.data.repositories.OrderItemRepo import OrderItemRepo
import stripe.error


class CheckingService:
    @staticmethod
    def checking(
        user: User,
        order: Order,
        payment_method_id: str,
        payment_method_type: str,
    ):
        customer_id = user.stripe_id
        payment_method = PaymentMethodService.get_by_name(payment_method_type)

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
                    payment_method=payment_method_id,
                    confirm=True,
                    metadata={"order_id": str(order.id)},
                )
            except stripe.error.StripeError as e:
                raise HttpError(400, f"One-time payment error: {e.user_message}")
            payment = PaymentRepo.add(
                payment_method=payment_method,
                amount=amount,
                status=0,
                order=order,
                subscription=None,
                invoice_url=None,
            )
            payments.append(
                {
                    "type": "one_time",
                    "id": stripe_intent.id,
                    "clientSecret": stripe_intent.client_secret,
                }
            )

        if monthly:
            monthly_items = [
                {
                    "price": item.product.stripe_monthly_price_id,
                    "quantity": item.quantity,
                    "metadata": {"order_item_id": item.id},
                }
                for item in monthly
            ]

            payment = PaymentRepo.add(
                payment_method=payment_method,
                amount=sum(item.product.price * item.quantity for item in monthly),
                status=0,
                order=order,
                subscription=None,
                invoice_url=None,
            )

            try:
                stripe_subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=monthly_items,
                    default_payment_method=payment_method_id,
                    payment_behavior="default_incomplete",
                    payment_settings={"save_default_payment_method": "on_subscription"},
                    expand=["latest_invoice.confirmation_secret"],
                    metadata={"order_id": str(order.id), "payment_id": str(payment.id)},
                )
            except stripe.error.StripeError as e:
                raise HttpError(400, f"Monthly subscription error: {e.user_message}")
            client_secret = (
                stripe_subscription.latest_invoice.confirmation_secret.client_secret
            )
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

            if local_subscription:
                PaymentRepo.update_subscription(payment, local_subscription)
                stripe_items = stripe_subscription.get("items", {}).get("data", [])
                for stripe_item in stripe_items:
                    metadata_id = int(stripe_item.metadata.order_item_id)
                    order_item = OrderItemRepo.get_by_id(metadata_id)
                    sub_item = SubscriptionItemRepo.add(
                        subscription=local_subscription,
                        order_item=order_item,
                        stripe_item_id=stripe_item.id,
                        current_period_start=timezone.datetime.fromtimestamp(
                            stripe_item.current_period_start,
                            tz=timezone.get_current_timezone(),
                        ),
                        current_period_end=timezone.datetime.fromtimestamp(
                            stripe_item.current_period_end,
                            tz=timezone.get_current_timezone(),
                        ),
                        price_id=stripe_item.price.id,
                        quantity=stripe_item.quantity,
                    )
                    if not sub_item:
                        OrderService.update_order_status(order.id, 2)
            payments.append(
                {
                    "type": "monthly",
                    "stripe_id": stripe_subscription.id,
                    "id": local_subscription.id,
                    "clientSecret": client_secret,
                }
            )

        if yearly:
            yearly_items = [
                {
                    "price": item.product.stripe_yearly_price_id,
                    "quantity": item.quantity,
                    "metadata": {"order_item_id": item.id},
                }
                for item in yearly
            ]

            payment = PaymentRepo.add(
                payment_method=payment_method,
                amount=sum(item.product.price * item.quantity * 12 for item in yearly),
                status=0,
                order=order,
                subscription=None,
                invoice_url=None,
            )

            try:
                stripe_subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=yearly_items,
                    default_payment_method=payment_method_id,
                    payment_behavior="default_incomplete",
                    payment_settings={"save_default_payment_method": "on_subscription"},
                    expand=["latest_invoice.confirmation_secret"],
                    metadata={"order_id": str(order.id), "payment_id": str(payment.id)},
                )
            except stripe.error.StripeError as e:
                raise HttpError(400, f"Yearly subscription error: {e.user_message}")
            client_secret = (
                stripe_subscription.latest_invoice.confirmation_secret.client_secret
            )
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

            if local_subscription:
                PaymentRepo.update_subscription(payment, local_subscription)
                stripe_items = stripe_subscription.get("items", {}).get("data", [])
                for stripe_item in stripe_items:
                    metadata_id = int(stripe_item.metadata.order_item_id)
                    order_item = OrderItemRepo.get_by_id(metadata_id)
                    sub_item = SubscriptionItemRepo.add(
                        subscription=local_subscription,
                        order_item=order_item,
                        stripe_item_id=stripe_item.id,
                        current_period_start=timezone.datetime.fromtimestamp(
                            stripe_item.current_period_start,
                            tz=timezone.get_current_timezone(),
                        ),
                        current_period_end=timezone.datetime.fromtimestamp(
                            stripe_item.current_period_end,
                            tz=timezone.get_current_timezone(),
                        ),
                        price_id=stripe_item.price.id,
                        quantity=stripe_item.quantity,
                    )
                    if not sub_item:
                        OrderService.update_order_status(order.id, 2)
            payments.append(
                {
                    "type": "yearly",
                    "stripe_id": stripe_subscription.id,
                    "id": local_subscription.id,
                    "clientSecret": client_secret,
                }
            )

        if not payments:
            raise HttpError(400, "No payable items in this order")

        return payments

    # @staticmethod
    # def checking(
    #     user: User, order: Order
    # ) -> tuple[Subscription | Payment, PaymentIntent, int] | tuple[None, None, None]:
    #     try:
    #         if order.recurrence == 0:
    #             return CheckingService.payment_checking(user, order)
    #         else:
    #             return CheckingService.subscription_checking(user, order)
    #     except Exception as e:
    #         print(e)
    #         return None, None, None

    # @staticmethod
    # def payment_checking(
    #     user: User, order: Order
    # ) -> tuple[Payment, PaymentIntent] | None:
    #     try:
    #         order_items = OrderService.get_all_items(order)
    #         amount = sum([item.quantity * item.product.price for item in order_items])

    #         payment, payment_intent = PaymentService.add(
    #             amount=amount,
    #             status=0,
    #             order_id=order.id,
    #         )

    #         if payment and payment_intent:
    #             return payment, payment_intent, 0

    #     except Exception as e:
    #         print(e)
    #         return None, None, None

    # @staticmethod
    # def subscription_checking(
    #     user: User, order: Order
    # ) -> tuple[Subscription, PaymentIntent] | None:
    #     try:
    #         subsciption, client_secret = SubscriptionService.add(
    #             user_id=user.id,
    #             billing_address_id=order.billing_address.id,
    #             recurrence=order.recurrence,
    #             order_id=order.id,
    #         )

    #         if subsciption and client_secret:
    #             return subsciption, client_secret, 1

    #     except Exception as e:
    #         print(e)
    #         return None, None, None

    # @staticmethod
    # def cancel(result_id: int, result_type: int) -> bool:
    #     try:
    #         if result_type == 0:
    #             return PaymentService.delete(result_id)
    #         elif result_type == 1:
    #             return SubscriptionService.delete_subscription(result_id)
    #     except Exception as e:
    #         print(e)
    #         return None

    @staticmethod
    def stripe_webhook_event(event):
        from utils.Stripe import StripeUtils

        event_object = event["data"]["object"]
        event_type = event["type"]
        order_id = None

        if event_type.startswith("payment_intent"):
            order_id = event_object.get("metadata", {}).get("order_id")
            payment_id = event_object.get("metadata", {}).get("payment_id")
        if event_type.startswith("invoice"):
            order_id = event_object.get("metadata", {}).get("order_id")
            payment_id = event_object.get("metadata", {}).get("payment_id")
            if not order_id:
                order_id = (
                    event_object.get("parent", {})
                    .get("subscription_details", {})
                    .get("metadata", {})
                    .get("order_id")
                )
            if not payment_id:
                payment_id = (
                    event_object.get("parent", {})
                    .get("subscription_details", {})
                    .get("metadata", {})
                    .get("payment_id")
                )

        if not order_id:
            return {"status": "ignored"}

        if event["type"] == "payment_intent.succeeded":
            OrderService.update_price_at_sale_by_order_id(order_id)
            OrderService.update_order_status(order_id, status=5)
            PaymentService.update_status(payment_id, 4)

        elif event["type"] == "invoice.paid":
            invoice = event_object
            amount_paid = invoice.get("amount_paid", {})
            stripe_subscription_id = (
                invoice.get("parent", {})
                .get("subscription_details", {})
                .get("subscription", {})
            )
            hosted_invoice_url = invoice.get("hosted_invoice_url")

            try:
                stripe_subscription = StripeUtils.retrive_subscription(
                    stripe_subscription_id
                )
            except Exception as e:
                print(f"Could not retrieve subscription {stripe_subscription_id}: {e}")
                return {"status": "ignored"}

            OrderService.update_price_at_sale_by_order_id(order_id)
            OrderService.update_order_status(order_id, status=5)

            new_status = stripe_subscription["status"]
            subscription = SubscriptionRepo.update_by_stripe_id(
                id=stripe_subscription_id,
                status=new_status,
                last_invoice_url=hosted_invoice_url,
            )

            pending = PaymentService.get_pending_subscription(subscription)

            if pending:
                PaymentService.update_status(payment_id, 4)
                PaymentService.update_invoice(payment_id, hosted_invoice_url)
            else:
                PaymentRepo.add(
                    payment_method=PaymentService.get(payment_id).payment_method,
                    amount=amount_paid,
                    status=4,
                    order=OrderService.get_order_by_id(order_id),
                    subscription=subscription,
                    invoice_url=hosted_invoice_url,
                )

            for line in invoice.get("lines", {}).get("data", {}):
                subscription_item_id = (
                    line.get("parent", {})
                    .get("subscription_item_details", {})
                    .get("subscription_item")
                )
                new_start = line.get("period", {}).get("start", {})
                new_end = line.get("period", {}).get("end", {})

                SubscriptionItemRepo.update_periods_by_stripe_id(
                    stripe_item_id=subscription_item_id,
                    new_start=new_start,
                    new_end=new_end,
                )

        elif event["type"] in (
            "payment_intent.payment_failed",
            "invoice.payment_failed",
        ):
            OrderService.update_order_status(order_id, status=2)
            PaymentService.update_status(payment_id, 1)
        elif event["type"] == "customer.subscription.deleted":
            OrderService.update_order_status(order_id, status=3)
            PaymentService.update_status(payment_id, 2)

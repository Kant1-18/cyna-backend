from payments.models import Subscription, PaymentMethod, Payment
from payments.src.services.SubscriptionService import SubscriptionService
from payments.src.services.PaymentService import PaymentService
from shop.models import Order, OrderItem, Product
from shop.src.services.OrderService import OrderService
from users.models import User
from stripe import PaymentIntent
from payments.src.data.repositories.SubscriptionItemRepo import SubscriptionItemRepo
from payments.src.data.repositories.SubscriptionRepo import SubscriptionRepo
from payments.src.data.repositories.PaymentRepo import PaymentRepo


class CheckingService:

    @staticmethod
    def checking(
        user: User, order: Order
    ) -> tuple[Subscription | Payment, PaymentIntent, int] | tuple[None, None, None]:
        try:
            if order.recurrence == 0:
                return CheckingService.payment_checking(user, order)
            else:
                return CheckingService.subscription_checking(user, order)
        except Exception as e:
            print(e)
            return None, None, None

    @staticmethod
    def payment_checking(
        user: User, order: Order
    ) -> tuple[Payment, PaymentIntent] | None:
        try:
            order_items = OrderService.get_all_items(order)
            amount = sum([item.quantity * item.product.price for item in order_items])

            payment, payment_intent = PaymentService.add(
                amount=amount,
                status=0,
                order_id=order.id,
            )

            if payment and payment_intent:
                return payment, payment_intent, 0

        except Exception as e:
            print(e)
            return None, None, None

    @staticmethod
    def subscription_checking(
        user: User, order: Order
    ) -> tuple[Subscription, PaymentIntent] | None:
        try:
            subsciption, client_secret = SubscriptionService.add(
                user_id=user.id,
                billing_address_id=order.billing_address.id,
                recurrence=order.recurrence,
                order_id=order.id,
            )

            if subsciption and client_secret:
                return subsciption, client_secret, 1

        except Exception as e:
            print(e)
            return None, None, None

    @staticmethod
    def cancel(result_id: int, result_type: int) -> bool:
        try:
            if result_type == 0:
                return PaymentService.delete(result_id)
            elif result_type == 1:
                return SubscriptionService.delete_subscription(result_id)
        except Exception as e:
            print(e)
            return None

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

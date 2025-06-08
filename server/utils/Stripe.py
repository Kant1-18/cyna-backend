import stripe
from shop.models import Order
from shop.src.services.OrderService import OrderService
from payments.src.services.PaymentMethodService import PaymentMethodService
from ninja.errors import HttpError
from config.settings import STRIPE_WEBHOOK_SECRET
from payments.src.data.repositories.SubscriptionRepo import SubscriptionRepo
from payments.src.data.repositories.SubscriptionItemRepo import SubscriptionItemRepo
from payments.src.services.PaymentService import PaymentService
from payments.src.data.repositories.PaymentRepo import PaymentRepo
from users.models import User


class StripeUtils:

    @staticmethod
    def create_product(name: str) -> stripe.Product | None:
        try:
            return stripe.Product.create(name=name)
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return None

    @staticmethod
    def add_monthly_price(stripe_product_id: str, price: int) -> stripe.Price | None:
        try:
            prices = stripe.Price.list(
                product=stripe_product_id, active=True, recurring={"interval": "month"}
            )
            for p in prices.auto_paging_iter():
                stripe.Price.modify(p.id, active=False)

            return stripe.Price.create(
                unit_amount=price,
                currency="eur",
                recurring={"interval": "month"},
                product=stripe_product_id,
            )
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return None

    @staticmethod
    def add_yealy_price(product_id: str, price: int) -> stripe.Price | None:
        try:
            prices = stripe.Price.list(
                product=product_id, active=True, recurring={"interval": "year"}
            )
            for p in prices.auto_paging_iter():
                stripe.Price.modify(p.id, active=False)

            return stripe.Price.create(
                unit_amount=price,
                currency="eur",
                recurring={"interval": "year"},
                product=product_id,
            )
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return None

    @staticmethod
    def delete_product(stripe_product_id: str) -> bool:
        try:
            active_prices = stripe.Price.list(product=stripe_product_id, active=True)
            inactive_prices = stripe.Price.list(product=stripe_product_id, active=False)

            for price in active_prices.auto_paging_iter():
                stripe.Price.delete(price.id)

            for price in inactive_prices.auto_paging_iter():
                stripe.Price.delete(price.id)

            stripe.Product.delete(stripe_product_id)
            return True

        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return False

    @staticmethod
    def create_customer(email: str, name: str) -> stripe.Customer | None:
        try:
            customer = stripe.Customer.create(email=email, name=name)
            return customer
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return None

    @staticmethod
    def delete_customer(customer_id: str) -> bool:
        try:
            stripe.Customer.delete(customer_id)
            return True
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return False

    @staticmethod
    def create_subscription(
        customer_id: str, recurrence: int, order: Order
    ) -> stripe.Subscription | None:
        try:
            payment_methods = [
                method.stripe_code for method in PaymentMethodService.get_all()
            ]
            order_items = OrderService.get_all_items(order)

            prices = []
            if recurrence == 1:
                for item in order_items:
                    if item.product.price <= 0:
                        raise ValueError("Stripe price cannot be 0 for subscription.")
                    prices.extend(
                        [
                            {
                                "price": item.product.stripe_monthly_price_id,
                                "quantity": item.quantity,
                            }
                        ]
                    )
            else:
                # elif recurrence == 2:
                for item in order_items:
                    if item.product.price <= 0:
                        raise ValueError("Stripe price cannot be 0 for subscription.")
                    prices.extend(
                        [
                            {
                                "price": item.product.stripe_yearly_price_id,
                                "quantity": item.quantity,
                            }
                        ]
                    )

            subscription = stripe.Subscription.create(
                customer=customer_id,
                payment_method_types=payment_methods,
                items=prices,
                payment_behavior="default_incomplete",
                payment_settings={"save_default_payment_method": "on_subscription"},
                expand=["latest_invoice.confirmation_secret"],
            )

            client_secret = (
                subscription.latest_invoice.confirmation_secret.client_secret
            )

            print(subscription)
            return subscription, client_secret

        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return None, None

    @staticmethod
    def create_payment_intent(
        amount: int, user_stripe_id: str
    ) -> stripe.PaymentIntent | None:
        try:
            payment_methods = [
                method.stripe_code for method in PaymentMethodService.get_all()
            ]
            payment_intent = stripe.PaymentIntent.create(
                payment_method_types=payment_methods,
                amount=amount,
                currency="eur",
                customer=user_stripe_id,
                automatic_payment_methods={"enabled": True},
            )
            return payment_intent
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return None

    @staticmethod
    def delete_subscription(subscription_id: str) -> bool:
        try:
            stripe.Subscription.delete(subscription_id)
            return True
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return False

    @staticmethod
    def delete_item_subscription(subscription_id: str, product_id: str) -> bool:
        try:
            stripe.SubscriptionItem.delete(subscription_id, product_id)
            return True
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return False

    @staticmethod
    def add_item_subscription(subscription_id: str, product_id: str) -> bool:
        try:
            stripe.SubscriptionItem.create(
                subscription=subscription_id, price=product_id
            )
            return True
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return False

    @staticmethod
    def webhook(request):
        payload = request.body
        sig_header = request.headers.get("Stripe-Signature", "")
        endpoint_secret = STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            raise HttpError(400, f"Webhook error : {str(e)}")

        try:
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
                    stripe_subscription = stripe.Subscription.retrieve(
                        stripe_subscription_id, expand=["latest_invoice"]
                    )
                except Exception as e:
                    print(
                        f"Could not retrieve subscription {stripe_subscription_id}: {e}"
                    )
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
        except Exception as e:
            print(f"Error processing webhook {event['type']}: {e}")
            raise HttpError(400, f"Webhook error : {str(e)}")

        return {"status": "success"}

    @staticmethod
    def create_setup_intent(user: User, order_id: int) -> stripe.SetupIntent | None:
        try:
            payment_methods = PaymentMethodService.get_all()
            payment_method_types = []
            if payment_methods:
                payment_method_types = [
                    payment_method.stripe_code for payment_method in payment_methods
                ]
            else:
                payment_method_types = ["card", "link", "sepa_debit"]

            return stripe.SetupIntent.create(
                customer=user.stripe_id,
                payment_method_types=payment_method_types,
                metadata={"order_id": str(order_id)},
            )
        except Exception as e:
            print(f"[Stripe ERROR]: {e}")
            return None

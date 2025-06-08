from stripe import stripe, PaymentIntent
from shop.models import Order
from shop.src.services.OrderService import OrderService
from payments.src.services.PaymentMethodService import PaymentMethodService
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

    @staticmethod
    def retrive_subscription(stripe_subscription_id: str) -> stripe.Subscription | None:
        return stripe.Subscription.retrieve(
            stripe_subscription_id, expand=["latest_invoice"]
        )

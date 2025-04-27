import stripe
from shop.models import Product


class Stripe:

    @staticmethod
    def create_product(name: str) -> stripe.Product | None:
        try:
            return stripe.Product.create(name=name)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def add_monthly_price(stripe_product_id: str, price: int) -> stripe.Price | None:
        try:
            prices = stripe.Price.list(product=stripe_product_id, active=True)
            for p in prices.auto_paging_iter():
                stripe.Price.modify(p.id, active=False)

            return stripe.Price.create(
                unit_amount=price,
                currency="eur",
                recurring={"interval": "month"},
                product=stripe_product_id,
            )
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def add_yealy_price(product_id: str, price: int) -> stripe.Price | None:
        try:
            prices = stripe.Price.list(product=product_id, active=True)
            for p in prices.auto_paging_iter():
                stripe.Price.modify(p.id, active=False)

            return stripe.Price.create(
                unit_amount=price,
                currency="eur",
                recurring={"interval": "year"},
                product=product_id,
            )
        except Exception as e:
            print(e)
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
            print(e)
            return False

    @staticmethod
    def create_customer(email: str, name: str) -> stripe.Customer | None:
        try:
            customer = stripe.Customer.create(email=email, name=name)
            return customer
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def delete_customer(customer_id: str) -> bool:
        try:
            stripe.Customer.delete(customer_id)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def create_subscription(
        customer_id: str, recurrence: bool, products: list[Product]
    ) -> stripe.Subscription | None:
        try:
            if not recurrence:
                prices = [product.stripe_monthly_price_id for product in products]
            else:
                prices = [product.stripe_yearly_price_id for product in products]

            items = [{"price": price} for price in prices]
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=items,
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
            )
            return subscription

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def create_payment_intent(
        amount: int, user_stripe_id: str
    ) -> stripe.PaymentIntent | None:
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="eur",
                customer=user_stripe_id,
                automatic_payment_methods={"enabled": True},
            )
            return payment_intent
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def delete_subscription(subscription_id: str) -> bool:
        try:
            stripe.Subscription.delete(subscription_id)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_item_subscription(subscription_id: str, product_id: str) -> bool:
        try:
            stripe.SubscriptionItem.delete(subscription_id, product_id)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def add_item_subscription(subscription_id: str, product_id: str) -> bool:
        try:
            stripe.SubscriptionItem.create(
                subscription=subscription_id, price=product_id
            )
            return True
        except Exception as e:
            print(e)
            return False

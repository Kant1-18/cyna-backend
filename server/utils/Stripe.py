from config.settings import STRIPE_API_KEY
import stripe
from shop.models import Product

stripe.api_key = STRIPE_API_KEY


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

            # Crée le nouveau prix
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

            # Crée le nouveau prix
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
    def create_customer(email: str, name: str, address: dict) -> stripe.Customer | None:
        try:
            customer = stripe.Customer.create(email=email, name=name, address=address)
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

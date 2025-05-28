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


class CheckingControl:
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

        items = OrderService.get_all_items(order)
        one_time = [item for item in items if item.recurring == 0]
        monthly = [item for item in items if item.recurring == 1]
        yearly = [item for item in items if item.recurring == 2]

        payments: list[dict] = []

        if one_time:
            amount = sum(item.product.price * item.quantity for item in one_time)
            try:
                intent = stripe.PaymentIntent.create(
                    customer=customer_id,
                    amount=amount,
                    currency="eur",
                    payment_method=data.paymentMethodId,
                    confirm=True,
                    metadata={"order_id": str(order.id)}
                )
            except stripe.error.StripeError as e:
                raise HttpError(400, f"One-time payment error: {e.user_message}")
            payments.append({
                "type": "one_time",
                "id": intent.id,
                "clientSecret": intent.client_secret,
            })

        if monthly:
            monthly_items = [{"price": item.product.stripe_monthly_price_id, "quantity": item.quantity} for item in monthly]
            try:
                subscription = stripe.Subscription.create(
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
            client_secret = subscription.latest_invoice.confirmation_secret.client_secret
            payments.append({
                "type": "monthly",
                "id": subscription.id,
                "clientSecret": client_secret,
            })

        if yearly:
            yearly_items = [{"price": item.product.stripe_yearly_price_id, "quantity": item.quantity} for item in yearly]
            try:
                subscription = stripe.Subscription.create(
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
            client_secret = subscription.latest_invoice.confirmation_secret.client_secret
            payments.append({
                "type": "yearly",
                "id": subscription.id,
                "clientSecret": client_secret,
            })

        if not payments:
            raise HttpError(400, "No payable items in this order")

        return {"payments": payments}
    
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

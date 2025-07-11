from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from shop.models import Order
from payments.models import Subscription
from users.models import User
from utils.emailTokens import generate_token, VERIFY_SALT, RESET_SALT
from django.conf import settings


def send_receipt(user_email: str, subscription: Subscription):
    try:
        items = subscription.items.all()
        total_cents = sum(item.order_item.product.price * item.quantity * (12 if item.order_item.recurring == 2 else 1)  for item in items)
        total = total_cents / 100

        html = render_to_string(
            "receipt.html",
            {
                "customer_name": f"{subscription.user.first_name} {subscription.user.last_name}",
                "billing_name": f"{subscription.user.first_name} {subscription.user.last_name}",
                "billing_address_line1": f"{subscription.billing_address.number}, {subscription.billing_address.street}",
                "billing_address_line2": f"{subscription.billing_address.complement}",
                "billing_zipcode": f"{subscription.billing_address.zip_code}",
                "billing_city": f"{subscription.billing_address.city}",
                "billing_region": f"{subscription.billing_address.region}",
                "billing_country": f"{subscription.billing_address.country}",
                "order": subscription,
                "items": [
                    {
                        "product": item.order_item.product,
                        "quantity": item.quantity,
                        "total": (item.quantity * item.order_item.product.price) * (12 if item.order_item.recurring == 2 else 1) / 100,
                    }
                    for item in items
                ],
                "total": total,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
        )

        msg = EmailMultiAlternatives(
            subject=f"Invoice for Subscription #{subscription.id}",
            body="Please find your subscription invoice attached.",
            from_email="cyna.b3pe@gmail.com",
            to=[user_email],
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

    except Exception as e:
        print("send_receipt error:", e)

def send_order_invoice(user_email: str, order: Order):
    try:
        items = order.items.all()
        total = sum(item.product.price * item.quantity for item in items) / 100

        html = render_to_string(
            "invoice.html",
            {
                "order": order,
                "items": [
                    {
                        "product": item.product,
                        "quantity": item.quantity,
                        "total": (item.quantity * item.product.price) / 100,
                    }
                    for item in items
                ],
                "total": total,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
        )

        msg = EmailMultiAlternatives(
            subject=f"Invoice for Order #{order.id}",
            body="Your invoice attached.",
            from_email="cyna.b3pe@gmail.com",
            to=[user_email],
        )

        msg.attach_alternative(html, "text/html")
        msg.send()
    except Exception as e:
        print(e)


def send_subscription_invoice(user_email: str, subscription: Subscription):
    try:
        items = subscription.items.all()
        total = sum(item.product.price * item.quantity for item in items) / 100
        html = render_to_string(
            "invoice.html",
            {
                "order": subscription,
                "items": [
                    {
                        "product": item.product,
                        "quantity": item.quantity,
                        "total": (item.quantity * item.product.price) / 100,
                    }
                    for item in items
                ],
                "total": total,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
        )

        msg = EmailMultiAlternatives(
            subject=f"Invoice for Subscription #{subscription.id}",
            body="Please find your subscription invoice attached.",
            from_email="cyna.b3pe@gmail.com",
            to=[user_email],
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
    except Exception as e:
        print(e)


def send_verification(user_email: str) -> None:
    token = generate_token(user_email, VERIFY_SALT)
    verification_url = f"{settings.FRONTEND_URL}/verify-account?token={token}"

    html = render_to_string(
        "verify_account.html", {"verification_url": verification_url}
    )

    msg = EmailMultiAlternatives(
        "Vérifiez votre compte", "", settings.DEFAULT_FROM_EMAIL, [user_email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


def send_password_reset(user_email: str) -> None:
    token = generate_token(user_email, RESET_SALT)
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    html = render_to_string(
        "reset_password.html",
        {
            "reset_url": reset_url,
            "token": token,
        },
    )

    msg = EmailMultiAlternatives(
        "Réinitialisation de mot de passe",
        "",
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()

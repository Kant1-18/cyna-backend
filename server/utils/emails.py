from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from shop.models import Order
from payments.models import Subscription
from users.models import User


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


def send_verification_email(user: User, token: str):
    try:
        verification_link = (
            f"https://your-frontend-domain.com/verify-account?token={token}"
        )
        html_content = render_to_string(
            "emails/verify_account.html",
            {"user": user, "verification_link": verification_link},
        )

        email = EmailMultiAlternatives(
            subject="Verify Your Account",
            body="Please verify your account.",
            from_email="cyna.b3pe@gmail.com",
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(f"Verification email error: {e}")


def send_password_reset_email(user: User, token: str):
    try:
        reset_link = f"https://your-frontend-domain.com/reset-password?token={token}"
        html_content = render_to_string(
            "emails/reset_password.html",
            {"user": user, "reset_link": reset_link},
        )

        email = EmailMultiAlternatives(
            subject="Reset Your Password",
            body="Follow the link to reset your password.",
            from_email="cyna.b3pe@gmail.com",
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(f"Password reset email error: {e}")

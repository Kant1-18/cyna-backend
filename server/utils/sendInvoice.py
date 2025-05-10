from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from shop.models import Order
from payments.models import Subscription


def send_order_invoice(user_email: str, order: Order):
    try:
        items = order.items.all()
        total = sum(item.product.price * item.quantity for item in items)
        print("coucou")
        html = render_to_string(
            "invoice.html",
            {
                "order": order,
                "items": [
                    {
                        "product": item.product,
                        "quantity": item.quantity,
                        "total": item.quantity * item.product.price,
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
        print("sending")
        msg.attach_alternative(html, "text/html")
        msg.send()
    except Exception as e:
        print(e)


def send_subscription_invoice(user_email: str, subscription: Subscription):
    try:
        items = subscription.items.all()
        total = sum(item.product.price * item.quantity for item in items)
        html = render_to_string(
            "invoice.html",
            {
                "order": subscription,  # même variable dans le template
                "items": [
                    {
                        "product": item.product,
                        "quantity": item.quantity,
                        "total": item.quantity * item.product.price,
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

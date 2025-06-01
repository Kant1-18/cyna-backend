from django.db import models
from payments.models import PaymentMethod
from users.models import User, Address


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ("active", ("Active")),
        ("canceled", ("Canceled")),
        ("ended", ("Ended")),
        ("incomplete", ("Incomplete")),
        ("incomplete_expired", ("Incomplete Expired")),
        ("past_due", ("Past Due")),
        ("paused", ("Paused")),
        ("trialing", ("Trialing")),
        ("unpaid", ("Unpaid")),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="incomplete")
    order_id = models.IntegerField(null=True, blank=True)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    recurrence = models.IntegerField(default=0)
    default_payment_method_id = models.CharField(max_length=255, null=True, blank=True)
    last_invoice_url = models.CharField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # temp cause some don't have due to tests (billingAddress + paymentMethod)
    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.to_json(),
            "status": self.status,
            "orderId": self.order_id,
            "billingAddress": self.billing_address.to_json() if self.billing_address else None,
            "paymentMethod": self.payment_method.to_json() if self.payment_method else None,
            "stripeSubscriptionId": self.stripe_subscription_id,
            "recurrence": self.recurrence,    
            "defaultPaymentMethodId": self.default_payment_method_id,
            "items": [item.to_json() for item in self.items.all()],
            "lastInvoiceUrl": self.last_invoice_url,
        }

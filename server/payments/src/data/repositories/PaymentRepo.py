from payments.models import Payment, PaymentMethod, Subscription
from shop.models import Order
from django.db.models.functions import TruncDate, TruncWeek
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta, date
from collections import defaultdict



class PaymentRepo:
    @staticmethod
    def add(
        payment_method: PaymentMethod,
        amount: int,
        status: int = 0,
        order: Order = None,
        subscription: Subscription = None,
    ) -> Payment | None:
        try:
            payment = Payment.objects.create(
                payment_method=payment_method,
                amount=amount,
                status=status,
                order=order,
                subscription=subscription,
            )
            if payment:
                return payment
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def get_sales_metrics(period: str, count: int):
        today = timezone.now().date()

        if period == "daily":
            start_date = today - timedelta(days=(count - 1))
            full_periods = [start_date + timedelta(days=i) for i in range(count)]

        elif period == "weekly":
            this_monday = today - timedelta(days=today.weekday())
            start_date = this_monday - timedelta(weeks=(count - 1))
            full_periods = [start_date + timedelta(weeks=i) for i in range(count)]
        else:
            return None

        query = (
            Payment.objects
            .filter(status=4, created_at__date__gte=start_date)
            .annotate(period_start=TruncDate("created_at"))
            .values("period_start")
            .annotate(total_amount=Sum("amount"), sale_count=Count("id"))
            .order_by("period_start")
        )

        daily_map = { entry["period_start"]: { "amount": entry["total_amount"] or 0, "count": entry["sale_count"] or 0 } for entry in query }

        if period == "daily":
            return [{ "period": period_date, "amount": daily_map.get(period_date, {"amount": 0})["amount"], "count": daily_map.get(period_date, {"count": 0})["count"] } for period_date in full_periods ]

        weekly_map = defaultdict(lambda: { "amount": 0, "count": 0 })
        for day, values in daily_map.items():
            monday = day - timedelta(days=day.weekday())
            weekly_map[monday]["amount"] += values["amount"]
            weekly_map[monday]["count"] += values["count"]

        return [{ "period": monday, "amount": weekly_map[monday]["amount"], "count": weekly_map[monday]["count"]} for monday in full_periods]

    @staticmethod
    def get(id: int) -> Payment | None:
        try:
            payment = Payment.objects.get(id=id)
            if payment:
                return payment
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_order(order: Order) -> list[Payment] | None:
        try:
            payments = Payment.objects.filter(order=order)
            if payments:
                return payments
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> list[Payment] | None:
        try:
            payments = Payment.objects.all()
            if payments:
                return payments
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def get_all_from_user(user_id: int):
        try:
            payments = Payment.objects.filter(order__user_id=user_id).select_related("payment_method", "order__shipping_address", "order__billing_address", "subscription")
            if payments:
                return payments
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def get_all_by_subscription(subscription: Subscription) -> list[Payment] | None:
        try:
            payments = Payment.objects.filter(subscription=subscription)
            if payments:
                return payments
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_status(payment: Payment, status: int) -> Payment | None:
        try:
            payment.status = status
            payment.save()
            return payment
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def update_subscription(payment: Payment, subscription: Subscription) -> Payment | None:
        try:
            payment.subscription = subscription
            payment.save()
            return payment
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete(payment: Payment) -> bool:
        try:
            payment.delete()
            return True
        except Exception as e:
            print(e)

        return False

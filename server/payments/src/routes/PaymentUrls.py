from datetime import datetime
from typing import List
from ninja.errors import HttpError
from ninja import Query, Router, ModelSchema, Schema
from payments.models import Payment
from payments.src.controllers.PaymentControl import PaymentControl
from ninja_jwt.authentication import JWTAuth

router = Router()


class PaymentSchema(ModelSchema):
    class Meta:
        model = Payment
        fields = "__all__"


class AddPaymentSchema(Schema):
    amount: int
    status: int
    orderId: int | None
    subscriptionId: int | None


class UpdateStatusSchema(Schema):
    id: int
    status: int

class SalesMetricPoint(Schema):
    period: datetime
    amount: int
    count: int

class SalesMetricsByCategoryPoint(Schema):
    category: str
    amount: int
    count: int

class SalesMetricsParams(Schema):
    period: str = "daily"
    count: int = 7

class SalesMetricsByCategoryParams(Schema):
    period: str = "daily"
    count: int = 7
    locale: str

@router.post("", auth=JWTAuth())
def add(request, data: AddPaymentSchema) -> Payment | HttpError:
    return PaymentControl.add(data)


@router.get("", auth=JWTAuth())
def get_all(request) -> list[Payment] | HttpError:
    return PaymentControl.get_all(request)

@router.get("/metrics/sales", auth=JWTAuth(), response=List[SalesMetricPoint])
def get_sales_metrics(request, params: Query[SalesMetricsParams]):
    return PaymentControl.get_sales_metrics(request, params)

@router.get("/metrics/categories", auth=JWTAuth(), response=List[SalesMetricsByCategoryPoint])
def get_sales_metrics_by_category(request, params: Query[SalesMetricsByCategoryParams]):
    return PaymentControl.get_sales_metrics_by_category(request, params)

@router.patch("/status", auth=JWTAuth())
def update_status(request, data: UpdateStatusSchema) -> Payment | HttpError:
    return PaymentControl.update_status(data)

@router.get("/user", auth=JWTAuth())
def get_all_from_user(request):
    return PaymentControl.get_all_from_user(request)

@router.get("/subscription/{subscription_id}", auth=JWTAuth())
def get_by_subscription(request, subscription_id: int) -> Payment | HttpError:
    return PaymentControl.get_by_subscription(request, subscription_id)


@router.get("/order/{order_id}", auth=JWTAuth())
def get_by_order(request, order_id: int) -> Payment | HttpError:
    return PaymentControl.get_by_order(order_id)


@router.get("/{id}", auth=JWTAuth())
def get(request, id: int) -> Payment | HttpError:
    return PaymentControl.get(id)


@router.delete("/{id}", auth=JWTAuth())
def delete(request, id: int) -> bool:
    return PaymentControl.delete(request, id)

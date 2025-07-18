from shop.models import Order, OrderItem
from shop.src.controllers.OrderControl import OrderControl
from ninja import Router, ModelSchema, Schema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from shop.src.data.models.Order import Order as OrderModel
from shop.src.data.models.OrderItem import OrderItem as OrderItemModel

router = Router()


class OrderSchema(ModelSchema):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSchema(ModelSchema):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderRouteSchema(Schema):
    productId: int
    quantity: int
    recurring: int

class OrderItemRouteSchema(Schema):
    id: int
    productId: int
    quantity: int
    recurring: int

class OrderUpdateSchema(Schema):
    orderId: int
    status: int
    shippingAddressId: int
    billingAddressId: int


class SratusUpdateSchema(Schema):
    orderId: int
    status: int


class OrderUpdateRecurrenceSchema(Schema):
    orderId: int
    recurrence: int


@router.post("/add-product", auth=JWTAuth())
def add_product(request, data: OrderRouteSchema) -> Order | HttpError:
    return OrderControl.add_product(request, data)


@router.put("/update-cart-item", auth=JWTAuth())
def update_product_in_cart(request, data: OrderItemRouteSchema) -> Order | HttpError:
    return OrderControl.update_product_in_cart(request, data)


@router.delete("/delete-cart-item/{item_id}", auth=JWTAuth())
def delete_product_from_cart(request, item_id: int) -> Order | HttpError:
    return OrderControl.delete_product_from_cart(request, item_id)


@router.get("/get-cart", auth=JWTAuth())
def get_cart(request) -> Order | HttpError:
    return OrderControl.get_cart(request)


@router.get("/get-all-orders", auth=JWTAuth())
def get_all_orders(request) -> list[Order] | HttpError:
    return OrderControl.get_all_orders(request)


@router.get("/get-order-by-id/{order_id}", auth=JWTAuth())
def get_order_by_id(request, order_id: int) -> Order | HttpError:
    return OrderControl.get_order_by_id(request, order_id)


@router.put("/update-order", auth=JWTAuth())
def update_order(request, data: OrderUpdateSchema) -> Order | HttpError:
    return OrderControl.update_order(request, data)


@router.patch("/update-order-status", auth=JWTAuth())
def update_order_status(request, data: SratusUpdateSchema) -> Order | HttpError:
    return OrderControl.update_order_status(request, data)


@router.patch("/update-order-recurrence", auth=JWTAuth())
def update_order_recurrence(
    request, data: OrderUpdateRecurrenceSchema
) -> Order | HttpError:
    return OrderControl.update_order_recurrence(request, data)


@router.delete("/delete-order/{order_id}", auth=JWTAuth())
def delete_order(request, order_id: int) -> Order | HttpError:
    return OrderControl.delete_order(request, order_id)

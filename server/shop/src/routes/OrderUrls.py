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


class OrderUpdateSchema(Schema):
    orderId: int
    status: int
    shippingAddressId: int
    billingAddressId: int


class SratusUpdateSchema(Schema):
    orderId: int
    status: int


@router.post("/addProduct", auth=JWTAuth())
def add_product(request, data: OrderRouteSchema) -> Order | HttpError:
    return OrderControl.add_product(request, data)


@router.put("/updateCartItem", auth=JWTAuth())
def update_product_in_cart(request, data: OrderRouteSchema) -> Order | HttpError:
    return OrderControl.update_product_in_cart(request, data)


@router.delete("/deleteCartItem/{productId}", auth=JWTAuth())
def delete_product_from_cart(request, productId: int) -> Order | HttpError:
    return OrderControl.delete_product_from_cart(request, productId)


@router.get("/getCart", auth=JWTAuth())
def get_cart(request) -> Order | HttpError:
    return OrderControl.get_cart(request)


@router.get("/getAllOrders", auth=JWTAuth())
def get_all_orders(request) -> list[Order] | HttpError:
    return OrderControl.get_all_orders(request)


@router.get("/getOrderById/{orderId}", auth=JWTAuth())
def get_order_by_id(request, orderId: int) -> Order | HttpError:
    return OrderControl.get_order_by_id(request, orderId)


@router.put("/updateOrder", auth=JWTAuth())
def update_order(request, data: OrderUpdateSchema) -> Order | HttpError:
    return OrderControl.update_order(request, data)


@router.patch("/updateOrderStatus", auth=JWTAuth())
def update_order_status(request, data: SratusUpdateSchema) -> Order | HttpError:
    return OrderControl.update_order_status(request, data)


@router.delete("/deleteOrder/{orderId}", auth=JWTAuth())
def delete_order(request, orderId: int) -> Order | HttpError:
    return OrderControl.delete_order(request, orderId)

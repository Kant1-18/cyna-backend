from shop.models import Order, OrderItem
from shop.src.services.OrderService import OrderService
from users.src.services.AuthService import AuthService
from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos


class OrderControl:
    @staticmethod
    def control_schema(data):
        if not CheckInfos.is_positive_int(data.productId):
            return HttpError(400, "Invalid productId")
        if not CheckInfos.is_positive_int(data.quantity):
            return HttpError(400, "Invalid quantity")
        return None

    @staticmethod
    def add_product(request, data) -> Order | HttpError:
        try:
            error = OrderControl.control_schema(data)
            if error:
                return error

            token = AuthService.get_token(request)
            user = AuthService.get_user_by_access_token(token)

            order = OrderService.add_product(user.id, data.productId, data.quantity)
            if order and order is not None:
                return order.to_json()
        except Exception as e:
            print(e)
            raise HttpError(
                500, "An error occurred while adding the product to the cart"
            )

    @staticmethod
    def update_product_in_cart(request, data) -> Order | HttpError:
        try:
            error = OrderControl.control_schema(data)
            if error:
                return error

            token = AuthService.get_token(request)
            user = AuthService.get_user_by_access_token(token)

            order = OrderService.update_product_in_cart(
                user.id, data.productId, data.quantity
            )
            if order:
                return order.to_json()
        except Exception as e:
            print(e)
            raise HttpError(
                500, "An error occurred while updating the product in the cart"
            )

    @staticmethod
    def delete_product_from_cart(request, item_id: int) -> bool | HttpError:
        try:
            if not CheckInfos.is_positive_int(item_id):
                return HttpError(400, "Invalid item id")

            return OrderService.delete_product_from_cart(item_id)
        except Exception as e:
            print(e)
            raise HttpError(
                500, "An error occurred while deleting the product from the cart"
            )

    @staticmethod
    def get_cart(request) -> Order | HttpError:
        try:
            token = AuthService.get_token(request)
            user = AuthService.get_user_by_access_token(token)
            order = OrderService.get_cart(user.id)
            if order:
                return order.to_json()
            else:
                raise HttpError(404, "Cart not found")
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while getting the cart")

    @staticmethod
    def get_all_orders(request) -> list[Order] | HttpError:
        try:
            token = AuthService.get_token(request)
            user = AuthService.get_user_by_access_token(token)
            orders = OrderService.get_all_orders(user.id)
            if orders:
                return [order.to_json() for order in orders]
            else:
                raise HttpError(404, "No orders found")
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while getting all orders")

    @staticmethod
    def get_order_by_id(request, id: int) -> Order | HttpError:
        try:
            if not CheckInfos.is_positive_int(id):
                return HttpError(400, "Invalid id")

            order = OrderService.get_order_by_id(id)
            if order:
                return order.to_json()
            else:
                raise HttpError(404, "Order not found")
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while getting the order")

    @staticmethod
    def update_order(request, data):
        try:
            if not CheckInfos.is_positive_int(data.orderId):
                return HttpError(400, "Invalid orderId")

            if not CheckInfos.is_status_order(data.status):
                return HttpError(400, "Invalid status")

            if not CheckInfos.is_positive_int(data.shippingAddressId):
                return HttpError(400, "Invalid shippingAddressId")

            if not CheckInfos.is_positive_int(data.billingAddressId):
                return HttpError(400, "Invalid billingAddressId")

            order = OrderService.update_order(
                data.orderId,
                data.status,
                data.shippingAddressId,
                data.billingAddressId,
            )
            if order:
                return order.to_json()
            else:
                raise HttpError(404, "Order not found")
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while updating the order")

    @staticmethod
    def update_order_status(request, data):
        try:
            if not CheckInfos.is_positive_int(data.orderId):
                return HttpError(400, "Invalid orderId")

            if not CheckInfos.is_status_order(data.status):
                return HttpError(400, "Invalid status")

            order = OrderService.update_order_status(data.orderId, data.status)
            if order:
                return order.to_json()
            else:
                raise HttpError(404, "Order not found")
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while updating the order status")

    @staticmethod
    def delete_order(request, id: int):
        try:
            if not CheckInfos.is_positive_int(id):
                return HttpError(400, "Invalid id")

            return OrderService.delete_order(id)
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred while deleting the order")

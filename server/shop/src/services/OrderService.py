from shop.models import Order, OrderItem, Product
from shop.src.data.repositories.OrderRepo import OrderRepo
from shop.src.data.repositories.OrderItemRepo import OrderItemRepo
from shop.src.services.ProductService import ProductService
from users.src.data.repositories.UserRepo import UserRepo
from users.models import User


class OrderService:

    @staticmethod
    def is_cart_exist(user: User) -> bool:
        try:
            order = OrderRepo.get_by_user_and_status(user, 0)
            if order:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def is_cart(order_id: int) -> bool:
        try:
            order = OrderRepo.get_by_id(order_id)
            if order.status == 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def add_product(user_id: int, product_id: int, quantity: int) -> Order | None:
        try:
            user = UserRepo.get(user_id)
            if user:
                if not OrderService.is_cart_exist(user):
                    order = OrderRepo.add(user)
                else:
                    order = OrderRepo.get_by_user_and_status(user, 0)
                product = ProductService.get(product_id)
                OrderItemRepo.add(order, product, quantity)

                return order
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_items(order: Order) -> list[OrderItem] | None:
        try:
            order_items = OrderItemRepo.get_all_by_order(order)
            if order_items:
                return order_items
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_product_in_cart(
        user_id: int, product_id: int, quantity: int
    ) -> Order | None:
        try:
            order = OrderRepo.get_by_user_and_status(user_id, 0)
            if order:
                product = ProductService.get(product_id)
                if product:
                    order_item = OrderItemRepo.get_by_order_and_product(order, product)
                    if order_item:
                        OrderItemRepo.update(order_item, quantity)
                        return order
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete_product_from_cart(item_id: int) -> bool | None:
        try:
            return OrderItemRepo.delete(item_id)
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_cart(user_id: int) -> Order | None:
        try:
            order = OrderRepo.get_by_user_and_status(user_id, 0)
            if order:
                return order
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_orders(user_id: int) -> list[Order] | None:
        try:
            orders = OrderRepo.get_all_by_user(user_id)
            if orders:
                return orders
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_order_by_id(order_id: int) -> Order | None:
        try:
            order = OrderRepo.get_by_id(order_id)
            if order:
                return order
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_order(
        order_id: int,
        status: int,
        shipping_address: str,
        billing_address: str,
    ) -> Order | None:
        try:
            order = OrderRepo.update(
                order_id, status, shipping_address, billing_address
            )
            if order:
                return order
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_order_status(order_id: int, status: int) -> Order | None:
        try:
            order = OrderRepo.update_status(order_id, status)
            if order:
                return order
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_order_recurrence(order_id: int, recurrence: int) -> Order | None:
        try:
            order = OrderRepo.update_recurrence(order_id, recurrence)
            if order:
                return order
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete_order(order_id: int) -> Order | None:
        try:
            return OrderRepo.delete(order_id)
        except Exception as e:
            print(e)

        return None

from shop.models import Order
from users.models import User, Address


class OrderRepo:

    @staticmethod
    def add(user: User) -> Order | None:
        try:
            order = Order.objects.create(
                user=user,
                status=0,
                shipping_address=None,
                billing_address=None,
            )
            if order:
                return order

        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_id(id: int) -> Order | None:
        try:
            order = Order.get(id=id)
            if order:
                return order
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_user_and_status(user: User, status: int) -> Order | None:
        try:
            order = Order.objects.get(user=user, status=status)
            if order:
                return order
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_by_user(user: User) -> list[Order]:
        try:
            orders = Order.objects.filter(user=user)
            if orders:
                return orders
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(
        order_id: int, status: int, shipping_address: Address, billing_address: Address
    ) -> Order | None:
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.shipping_address = shipping_address
            order.billing_address = billing_address
            order.save()
            return order
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_status(order_id: int, status: int) -> Order | None:
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return order
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def delete(order_id: int) -> Order | None:
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return order
        except Exception as e:
            print(e)
            return None

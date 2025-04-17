from shop.models import Product, Order, OrderItem


class OrderItemRepo:

    @staticmethod
    def add(order: Order, product: Product, quantity: int) -> OrderItem | None:
        try:
            return OrderItem.create(order=order, product=product, quantity=quantity)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_by_id(id: int) -> OrderItem | None:
        try:
            item = OrderItem.get(id=id)
            if item:
                return item
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_by_order(order: Order) -> list[OrderItem]:
        try:
            items = OrderItem.objects.filter(order=order)
            if items:
                return items
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(order_item: OrderItem, quantity: int) -> OrderItem | None:
        try:
            order_item.quantity = quantity
            order_item.save()
            return order_item
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def delete(order_item: OrderItem) -> OrderItem | None:
        try:
            order_item.delete()
            return order_item
        except Exception as e:
            print(e)
            return None

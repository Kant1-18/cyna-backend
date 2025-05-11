from shop.models import Product, Order, OrderItem


class OrderItemRepo:

    @staticmethod
    def add(order: Order, product: Product, quantity: int) -> OrderItem | None:
        try:
            return OrderItem.objects.create(
                order=order, product=product, quantity=quantity
            )
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_by_id(id: int) -> OrderItem | None:
        try:
            item = OrderItem.objects.get(id=id)
            if item:
                return item
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_order_and_product(order: Order, product: Product) -> OrderItem | None:
        try:
            item = OrderItem.objects.get(order=order, product=product)
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
    def delete(order_item_id: int) -> bool | None:
        try:
            order_item_id = OrderItem.objects.get(id=order_item_id)
            if order_item_id:
                order_item_id.delete()
                return True
        except Exception as e:
            print(e)

        return False

from shop.src.data.models.Discount import Discount
from shop.src.data.models.Product import Product
from shop.src.services.ProductService import ProductService
from datetime import datetime


class DiscountRepo:

    @staticmethod
    def add(product: Product, percentage: int, end_date) -> Discount | None:
        try:
            discount_price = product.price - (product.price * percentage / 100)
            end_date = datetime.fromtimestamp(end_date)
            dicount = Discount.objects.create(
                product=product,
                percentage=percentage,
                discount_price=discount_price,
                end_date=end_date,
            )
            if dicount:
                return dicount
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get(id: int) -> Discount | None:
        try:
            discount = Discount.objects.get(id=id)
            if discount:
                return discount
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_active_by_product(product: Product) -> Discount | None:
        try:
            discounts = Discount.objects.filter(
                product=product, end_date__gte=datetime.now()
            )
            if discounts:
                return discounts
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> list[Discount] | None:
        try:
            discounts = Discount.objects.all()
            if discounts:
                return discounts
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_active() -> list[Discount] | None:
        try:
            discounts = Discount.objects.filter(end_date__gte=datetime.now())
            if discounts:
                return discounts
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(id: int, percentage: int, end_date) -> Discount | None:
        try:
            discount = Discount.objects.get(id=id)
            if discount:
                discount.percentage = percentage
                discount.end_date = datetime.fromtimestamp(end_date)
                discount.save()
                return discount
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete(id: int) -> bool:
        try:
            discount = Discount.objects.get(id=id)
            if discount:
                discount.delete()
                return discount
        except Exception as e:
            print(e)

        return None

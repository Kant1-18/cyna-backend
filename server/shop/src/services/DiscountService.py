from shop.src.data.models.Discount import Discount
from shop.src.data.repositories.DiscountRepo import DiscountRepo
from shop.src.services.ProductService import ProductService


class DiscountService:

    @staticmethod
    def add(product_id: int, percentage: int, end_date) -> Discount | None:
        product = ProductService.get(product_id)
        if product:
            return DiscountRepo.add(product, percentage, end_date)

    @staticmethod
    def get(id: int) -> Discount | None:
        return DiscountRepo.get(id)

    @staticmethod
    def get_active_by_product(product_id: int) -> Discount | None:
        product = ProductService.get(product_id)
        if product:
            return DiscountRepo.get_active_by_product(product)

        return None

    @staticmethod
    def get_all() -> list[Discount] | None:
        return DiscountRepo.get_all()

    @staticmethod
    def get_all_active() -> list[Discount] | None:
        return DiscountRepo.get_all_active()

    @staticmethod
    def update(id: int, percentage: int, end_date) -> Discount | None:
        return DiscountRepo.update(id, percentage, end_date)

    @staticmethod
    def delete(id: int) -> bool:
        return DiscountRepo.delete(id)

from shop.src.data.models.Product import Product
from shop.src.data.repositories.ProductRepo import ProductRepo
from shop.src.data.repositories.CategoryRepo import CategoryRepo
from shop.src.data.repositories.DiscountRepo import DiscountRepo


class ProductService:

    @staticmethod
    def add(
        name: str,
        descripton: str,
        price: int,
        status: int,
        category_id: int,
        image: str,
    ) -> Product | None:
        category = CategoryRepo.get(category_id)
        return ProductRepo.add(name, descripton, price, status, category, image)

    @staticmethod
    def get(id: int) -> Product | None:
        return ProductRepo.get(id)

    @staticmethod
    def get_all() -> list[Product] | None:
        return ProductRepo.get_all()

    @staticmethod
    def get_by_category(category_id: int) -> list[Product] | None:
        category = CategoryRepo.get(category_id)
        return ProductRepo.get_all_by_category(category)

    @staticmethod
    def update(
        id: int,
        name: str,
        descripton: str,
        price: int,
        status: int,
        category_id: int,
        image: str,
    ) -> Product | None:
        category = CategoryRepo.get(category_id)
        return ProductRepo.update(id, name, descripton, price, status, category, image)

    # @staticmethod
    # def update_top(id: int, top_order: int) -> (Product | None):
    #     return ProductRepo.update_top(id, top_order)

    @staticmethod
    def delete(id: int) -> bool:
        return ProductRepo.delete(id)

    @staticmethod
    def get_all_with_discounts() -> tuple | None:
        try:
            discounts = DiscountRepo.get_all_active()
            if discounts:
                discount_ids = [discount.product.id for discount in discounts]
                products = [
                    product
                    for product in ProductRepo.get_all()
                    if product.id not in discount_ids
                ]
                return (discounts, products)
            else:
                return None, ProductRepo.get_all()
        except Exception as e:
            print(e)

        return None, None

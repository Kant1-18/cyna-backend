from shop.src.data.models.Product import Product
from shop.src.data.repositories.ProductRepo import ProductRepo
from shop.src.data.repositories.CategoryRepo import CategoryRepo
from shop.src.data.repositories.DiscountRepo import DiscountRepo
from ninja.files import UploadedFile
from utils.cloudinary import ImageUploader


class ProductService:

    @staticmethod
    def add(
        name: str,
        description: str,
        price: int,
        status: int,
        category_id: int,
        image: UploadedFile,
    ) -> Product | None:
        category = CategoryRepo.get(category_id)
        if not category:
            return None

        try:
            image_url = ImageUploader.product(image)
            return ProductRepo.add(
                name, description, price, status, category, image_url
            )

        except Exception as e:
            print(f"[Cloudinary Upload Error] {e}")
            return None

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
        id: int, name: str, descripton: str, price: int, status: int, category_id: int
    ) -> Product | None:
        category = CategoryRepo.get(category_id)
        return ProductRepo.update(id, name, descripton, price, status, category)

    @staticmethod
    def update_image(id: int, image: str) -> bool:
        try:
            image_url = ImageUploader.product(image)
            return ProductRepo.update_image(id, image_url)
        except Exception as e:
            print(f"[Cloudinary Upload Error] {e}")
            return False

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

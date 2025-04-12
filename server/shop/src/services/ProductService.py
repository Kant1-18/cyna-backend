from shop.models import Product
from shop.models import ProductDetails as Details
from shop.src.data.repositories.ProductRepo import ProductRepo
from shop.src.data.repositories.ProductDetailsRepo import (
    ProductDetailsRepo as DetailsRepo,
)
from shop.src.data.repositories.CategoryRepo import CategoryRepo
from ninja.files import UploadedFile
from utils.cloudinary import ImageUploader


class ProductService:

    ###########################################################################
    # ADD
    ###########################################################################

    @staticmethod
    def add_product(
        category_id: int,
        status: int,
        base_price: int,
        image1: UploadedFile,
        image2: UploadedFile,
        image3: UploadedFile,
    ) -> Product | None:
        category = CategoryRepo.get(category_id)
        if not category:
            return None

        try:
            image1 = ImageUploader.product(image1)
            image2 = ImageUploader.product(image2)
            image3 = ImageUploader.product(image3)
            return ProductRepo.add(
                category,
                status,
                base_price,
                image1,
                image2,
                image3,
            )

        except Exception as e:
            print("creation errot", e)
            return None

    @staticmethod
    def add_details(
        product_id: int,
        locale: str,
        name: str,
        description_title: str,
        description_text: str,
        benefits: dict,
        functionalities: dict,
        specifications: dict,
    ) -> Details | None:
        product = ProductRepo.get(product_id)
        if not product:
            return None

        try:
            return DetailsRepo.add(
                product,
                locale,
                name,
                description_title,
                description_text,
                benefits,
                functionalities,
                specifications,
            )
        except Exception as e:
            print("creation errot", e)
            return None

    ###########################################################################
    # GET
    ###########################################################################

    @staticmethod
    def get(product_id: int) -> Product | None:
        return ProductRepo.get(product_id)

    @staticmethod
    def get_by_locale(product_id: int, locale: str) -> Product | None:
        try:
            product = ProductRepo.get(product_id)
            details = DetailsRepo.get_all_by_product_and_locale(product, locale)

            return product, details

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_all() -> list[Product] | None:
        return ProductRepo.get_all()

    @staticmethod
    def get_all_by_locale(locale: str) -> list[Product] | None:
        result = {}
        try:
            products = ProductRepo.get_all()
            for product in products:
                details = DetailsRepo.get_all_by_product_and_locale(product, locale)
                result[product] = details

            return result
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_all_by_category(category_id: int) -> list[Product] | None:
        category = CategoryRepo.get(category_id)
        if not category:
            return None
        return ProductRepo.get_all_by_category(category)

    @staticmethod
    def get_all_by_category_and_status(
        category_id: int, status: int
    ) -> list[Product] | None:
        category = CategoryRepo.get(category_id)
        if not category:
            return None
        return ProductRepo.get_all_by_category_and_status(category, status)

    @staticmethod
    def get_all_by_status(status: int) -> list[Product] | None:
        return ProductRepo.get_all_by_status(status)

    ###########################################################################
    # UPDATE
    ###########################################################################

    @staticmethod
    def update_product(
        product_id: int,
        category_id: int,
        status: int,
        base_price: int,
        discount_order: int,
        discount_percentage: int,
    ) -> Product | None:
        category = CategoryRepo.get(category_id)
        if not category:
            return None

        try:
            return ProductRepo.update(
                product_id,
                category,
                status,
                base_price,
                discount_order,
                discount_percentage,
            )
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_details(product_id: int, locale: str, details: dict) -> Details | None:
        product = ProductRepo.get(product_id)
        details = DetailsRepo.get_all_by_product_and_locale(product, locale)
        ...

    @staticmethod
    def update_image1(id: int, image: str) -> bool:
        try:
            image_url = ImageUploader.product(image)
            return ProductRepo.update_image1(id, image_url)
        except Exception as e:
            print(f"[Cloudinary Upload Error] {e}")
            return False

    @staticmethod
    def update_image2(id: int, image: str) -> bool:
        try:
            image_url = ImageUploader.product(image)
            return ProductRepo.update_image2(id, image_url)
        except Exception as e:
            print(f"[Cloudinary Upload Error] {e}")
            return False

    @staticmethod
    def update_image3(id: int, image: str) -> bool:
        try:
            image_url = ImageUploader.product(image)
            return ProductRepo.update_image3(id, image_url)
        except Exception as e:
            print(f"[Cloudinary Upload Error] {e}")
            return False

    ###########################################################################
    # delete
    ###########################################################################

    @staticmethod
    def delete(id: int) -> bool:
        return ProductRepo.delete(id)

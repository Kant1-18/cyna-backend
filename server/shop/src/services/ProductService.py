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
        name: str,
        type: int,
        status: int,
        base_price: int,
        price: int,
        discount_order: int,
        discount_percentage: int,
        image1: UploadedFile,
        image2: UploadedFile,
        image3: UploadedFile,
    ) -> Product | None:
        from utils.Stripe import StripeUtils

        category = CategoryRepo.get(category_id)
        if not category:
            return None

        try:
            stripe_product = StripeUtils.create_product(name)
            stripe_monthly_price = StripeUtils.add_monthly_price(
                stripe_product.id, base_price
            )
            stripe_yearly_price = StripeUtils.add_yealy_price(
                stripe_product.id, (base_price * 12)
            )

            image1 = ImageUploader.product(image1)
            image2 = ImageUploader.product(image2)
            image3 = ImageUploader.product(image3)
            return ProductRepo.add(
                category,
                name,
                type,
                status,
                base_price,
                price,
                discount_order,
                discount_percentage,
                image1,
                image2,
                image3,
                stripe_id=stripe_product.id,
                stripe_monthly_price_id=stripe_monthly_price.id,
                stripe_yearly_price_id=stripe_yearly_price.id,
            )

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def add_product_details(
        product_id: int,
        locale: str,
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
                description_title,
                description_text,
                benefits,
                functionalities,
                specifications,
            )
        except Exception as e:
            print(e)
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
            details = DetailsRepo.get_by_product_and_locale(product, locale)

            return product, details

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_all_by_locale(locale: str) -> list[Product] | None:
        result_details = {}
        try:
            products = ProductRepo.get_all()
            for product in products:
                details = DetailsRepo.get_by_product_and_locale(product, locale)
                result_details[product] = details

            return products, result_details
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_all_by_category_and_locale(
        category_id: int, locale: str
    ) -> list[Product] | None:
        category = CategoryRepo.get(category_id)
        if not category:
            return None
        result_details = {}
        try:
            products = ProductRepo.get_all_by_category(category)
            for product in products:
                details = DetailsRepo.get_by_product_and_locale(product, locale)
                result_details[product] = details
            return products, result_details
        except Exception as e:
            print(e)
            return None

    ###########################################################################
    # UPDATE
    ###########################################################################

    @staticmethod
    def update_product(
        product_id: int,
        category_id: int,
        type: int,
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
                type,
                status,
                base_price,
                discount_order,
                discount_percentage,
            )
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_details(
        id: int,
        description_title: str,
        description_text: str,
        benefits: dict,
        functionalities: dict,
        specifications: dict,
    ) -> Details | None:
        try:
            return DetailsRepo.update(
                id,
                description_title,
                description_text,
                benefits,
                functionalities,
                specifications,
            )

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_image1(id: int, image) -> bool:
        try:
            image_url = ImageUploader.product(image)
            return ProductRepo.update_image1(id, image_url)
        except Exception as e:
            print(f"[Cloudinary Upload Error] {e}")
            return False

    @staticmethod
    def update_image2(id: int, image) -> bool:
        try:
            image_url = ImageUploader.product(image)
            return ProductRepo.update_image2(id, image_url)
        except Exception as e:
            print(f"[Cloudinary Upload Error] {e}")
            return False

    @staticmethod
    def update_image3(id: int, image) -> bool:
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
    def delete_product(id: int) -> bool:
        return ProductRepo.delete(id)

    @staticmethod
    def delete_details(id: int) -> bool:
        return DetailsRepo.delete(id)

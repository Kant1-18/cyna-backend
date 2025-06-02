from shop.models import Product
from shop.models import ProductDetails as Details
from shop.src.data.repositories.ProductRepo import ProductRepo
from shop.src.data.repositories.ProductDetailsRepo import (
    ProductDetailsRepo as DetailsRepo,
)
from shop.src.data.repositories.CategoryRepo import CategoryRepo
from ninja.files import UploadedFile
from utils.Cloudinary import ImageUploader
import json


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
                stripe_product.id, int(round(base_price * (1 - discount_percentage / 100)))
            )
            stripe_yearly_price = StripeUtils.add_yealy_price(
                stripe_product.id, int(round((base_price * (1 - discount_percentage / 100)) * 12))
            )

            image1 = ImageUploader.product(image1)
            image2 = ImageUploader.product(image2)
            image3 = ImageUploader.product(image3)
            return ProductRepo.add(
                category=category,
                name=name,
                type=type,
                status=status,
                base_price=base_price,
                discount_order=discount_order,
                discount_percentage=discount_percentage,
                image1=image1,
                image2=image2,
                image3=image3,
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
        benefits,
        functionalities,
        specifications,
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
                json.dumps(benefits),
                json.dumps(functionalities),
                json.dumps(specifications),
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
    def get_all() -> list[Product] | None:
        try:
            products = ProductRepo.get_all()
            if products:
                return products
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def get_best_seller() -> Product | None:
        try:
            best = ProductRepo.get_best_seller()
            if best:
                return best
        except Exception as e:
            print(f"Error getting best seller: {e}")
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
        name: str,
        type: int,
        status: int,
        base_price: int,
        discount_order: int,
        discount_percentage: int,
    ) -> Product | None:
        from utils.Stripe import StripeUtils

        category = CategoryRepo.get(category_id)
        if not category:
            return None

        try:
            product = ProductRepo.get(id=product_id)
            if product:
                if (
                    discount_percentage != product.discount_percentage
                    or base_price != product.base_price
                ):
                    update_price = True
                else:
                    update_price = False

                if update_price:
                    new_monthly_price = StripeUtils.add_monthly_price(product.stripe_id, int(round(base_price * (1 - discount_percentage / 100))))
                    new_yearly_price = StripeUtils.add_yealy_price(
                        product.stripe_id, int(round((base_price * (1 - discount_percentage / 100)) * 12))
                    )

                ProductRepo.update(
                    product=product,
                    category=category,
                    name=name,
                    type=type,
                    status=status,
                    base_price=base_price,
                    discount_order=discount_order,
                    discount_percentage=discount_percentage,
                    stripe_monthly_price_id=new_monthly_price.id if update_price else product.stripe_monthly_price_id,
                    stripe_yearly_price_id=new_yearly_price.id  if update_price else product.stripe_yearly_price_id,
                )

                
                return product
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_details(
        id: int,
        description_title: str,
        description_text: str,
        benefits,
        functionalities,
        specifications,
    ) -> Details | None:
        try:
            return DetailsRepo.update(
                id,
                description_title,
                description_text,
                json.dumps(benefits),
                json.dumps(functionalities),
                json.dumps(specifications),
            )

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_image1(id: int, image) -> Product | None:
        try:
            image_url = ImageUploader.product(image)
            return ProductRepo.update_image1(id, image_url)
        except Exception as e:
            print(f"[Cloudinary Upload Error] {e}")
            return False

    @staticmethod
    def update_image2(id: int, image) -> Product | None:
        try:
            image_url = ImageUploader.product(image)
            return ProductRepo.update_image2(id, image_url)
        except Exception as e:
            print(f"[Cloudinary Upload Error] {e}")
            return False

    @staticmethod
    def update_image3(id: int, image) -> Product | None:
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

    ###########################################################################
    # check
    ###########################################################################

    @staticmethod
    def is_product_exist(product_id: int, locale: str) -> bool:
        try:
            product = ProductRepo.get(product_id)
            if product:
                return DetailsRepo.is_locale_exist(product, locale)

        except Exception as e:
            print(e)
            return False

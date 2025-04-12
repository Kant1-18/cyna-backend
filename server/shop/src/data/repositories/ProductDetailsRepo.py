from shop.models import ProductDetails
from shop.models import Product


class ProductDetailsRepo:

    @staticmethod
    def add(
        product: Product,
        locale: str,
        name: str,
        description_title: str,
        description_text: str,
        benefits: dict,
        functionalities: dict,
        specifications: dict,
    ) -> ProductDetails | None:
        try:
            product_details = ProductDetails.objects.create(
                product=product,
                locale=locale,
                name=name,
                description_title=description_title,
                description_text=description_text,
                benefits=benefits,
                functionalities=functionalities,
                specifications=specifications,
            )
            if product_details:
                return product_details
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get(id: int) -> ProductDetails | None:
        try:
            product_details = ProductDetails.objects.get(id=id)
            if product_details:
                return product_details
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_by_product_and_locale(
        product: Product, locale: str
    ) -> ProductDetails | None:
        try:
            product_details = ProductDetails.objects.get(product=product, locale=locale)
            if product_details:
                return product_details
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> list[ProductDetails] | None:
        try:
            product_details = ProductDetails.objects.all()
            if product_details:
                return product_details
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_by_product(product: Product) -> list[ProductDetails] | None:
        try:
            product_details = ProductDetails.objects.get(product=product)
            if product_details:
                return product_details
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_by_product(product: Product) -> list[ProductDetails] | None:
        try:
            product_details = ProductDetails.objects.filter(product=product)
            if product_details:
                return product_details
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(
        id: int,
        locale: str,
        name: str,
        description_title: str,
        description_text: str,
        benefits: dict,
        functionalities: dict,
        specifications: dict,
    ) -> ProductDetails | None:
        try:
            product_details = ProductDetails.objects.get(id=id)
            if product_details:
                product_details.locale = locale
                product_details.name = name
                product_details.description_title = description_title
                product_details.description_text = description_text
                product_details.benefits = benefits
                product_details.functionalities = functionalities
                product_details.specifications = specifications
                product_details.save()
                return product_details
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete(id: int) -> bool:
        try:
            product_details = ProductDetails.objects.get(id=id)
            if product_details:
                product_details.delete()
                return True
        except Exception as e:
            print(e)

        return False

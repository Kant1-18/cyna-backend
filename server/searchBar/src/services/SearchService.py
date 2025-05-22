from shop.models import Product, Category
from shop.src.services.ProductService import ProductService
from shop.src.services.CategoryService import CategoryService


class SearchService:

    @staticmethod
    def search_products(
        locale: str = "en",
        category_id: int | None = None,
        words: list[str] | None = None,
    ) -> list[Product] | None:
        try:
            result = []

            if category_id:
                products, details = ProductService.get_all_by_category_and_locale(
                    category_id, locale
                )

                if products and details:
                    for word in words:
                        for product in products:
                            if word.lower() == product.name.lower():
                                result.append(product)
                                products.pop(product)
            else:
                ...

        except Exception as e:
            print(e)
            return None

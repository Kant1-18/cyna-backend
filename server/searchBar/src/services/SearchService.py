from collections import defaultdict
from shop.models import Product, ProductDetails
from shop.src.services.ProductService import ProductService


class SearchService:

    @staticmethod
    def search_products(
        locale: str = "en",
        category_id: int | None = None,
        words: list[str] | None = None,
    ) -> list[Product] | None:
        try:
            if not words:
                return []

            words = [w.lower() for w in words]
            matched_products = defaultdict(int)

            if category_id:
                products, details = ProductService.get_all_by_category_and_locale(
                    category_id, locale
                )
            else:
                products, details = ProductService.get_all_by_locale(locale)

            for product in products:
                if product.status != 1:
                    continue

                name = product.name.lower()
                description = ""
                for detail in details:
                    if detail.product_id == product.id and detail.description:
                        description = detail.description.lower()
                        break

                if any(word == name for word in words):
                    matched_products[product] += 3
                    continue

                if any(word in name for word in words):
                    matched_products[product] += 2

                if any(word in description for word in words):
                    matched_products[product] += 1

            sorted_products = sorted(
                matched_products.items(), key=lambda x: x[1], reverse=True
            )
            return [product for product, _ in sorted_products]

        except Exception as e:
            print(e)
            return None

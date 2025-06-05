from collections import defaultdict
from shop.models import Product, ProductDetails
from shop.src.services.ProductService import ProductService


class SearchService:

    @staticmethod
    def search_products(
        words: list[str],
        locale: str = "en",
        category_id: int | None = None,
    ) -> list[Product]:
        matched_products: dict[Product, int] = defaultdict(int)

        if category_id is not None:
            result = ProductService.get_all_by_category_and_locale(category_id, locale)
        else:
            result = ProductService.get_all_by_locale(locale)

        if not result:
            return [], {}

        products, details_map = result

        for product in products:
            name_lower = (product.name or "").lower()

            product_details: ProductDetails | None = details_map.get(product)
            if not product_details:
                continue

            description_lower = ""
            parts = []
            if product_details.description_title:
                parts.append(product_details.description_title)
            if product_details.description_text:
                parts.append(product_details.description_text)
            if product_details.benefits:
                parts.append(product_details.benefits)
            if product_details.functionalities:
                parts.append(product_details.functionalities)
            if product_details.specifications:
                parts.append(product_details.specifications)

                description_lower = " ".join(parts).lower()

            if any(word == name_lower for word in words):
                matched_products[product] += 3
                continue

            if any(word in name_lower for word in words):
                matched_products[product] += 2

            if description_lower and any(word in description_lower for word in words):
                matched_products[product] += 1

        sorted_by_score = sorted(
            matched_products.items(),
            key=lambda pair: pair[1],
            reverse=True
        )

        return [product_found for product_found, _score in sorted_by_score], details_map

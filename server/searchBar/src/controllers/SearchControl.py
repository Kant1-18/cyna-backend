from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos
from shop.src.services.CategoryService import CategoryService
from searchBar.src.services.SearchService import SearchService
from shop.models import Product


class SearchControl:

    @staticmethod
    def search_products(
        request,
        locale: str = "en",
        category_id: int | None = None,
        words: list[str] | None = None,
    ) -> list[Product] | HttpError:
        try:
            if not CheckInfos.check_locale(locale):
                raise HttpError(400, "Invalid locale")
            if category_id is not None:
                if not CheckInfos.check_category_id(category_id):
                    raise HttpError(400, "Invalid category ID")
                if not CategoryService.get_category_by_id(category_id):
                    raise HttpError(404, "Category not found")

            products = SearchService.search_products(
                request, locale, category_id, words
            )
            if products:
                return [product.to_json_all() for product in products]
            else:
                raise HttpError(404, "No products found matching the search criteria")
        except Exception as e:
            raise HttpError(500, "An error occurred")

from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos
from shop.src.services.CategoryService import CategoryService
from searchBar.src.services.SearchService import SearchService
from shop.models import Product


class SearchControl:

    @staticmethod
    def search_products(
        words: list[str] | None = None,
        locale: str = "en",
        category_id: int | None = None,
    ) -> list[dict] | HttpError:
        if not CheckInfos.is_valid_locale(locale):
            raise HttpError(400, "Invalid locale")

        if category_id is not None:
            if not CheckInfos.is_positive_int(category_id):
                raise HttpError(400, "Invalid category ID")
            if not CategoryService.get(category_id):
                raise HttpError(404, "Category not found")
        
        if not words:
            return []

        try:
            products = SearchService.search_products(words, locale, category_id)
        except HttpError:
            raise
        except Exception as e:
            raise HttpError(500, f"Search failed: {str(e)}")

        if not products:
            return []

        return [product.to_json_all() for product in products]

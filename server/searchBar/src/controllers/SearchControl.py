from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos
from shop.src.services.CategoryService import CategoryService
from searchBar.src.services.SearchService import SearchService
from shop.models import Product


class SearchControl:

    @staticmethod
    def search_products(
        words: str | None = None,
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
            
        if words is None or not CheckInfos.is_valid_string(words):
            return []
        
        words_list = [word.strip().lower() for word in words.split() if word.strip()]
        if not words_list:
            return []

        try:
            products, details_map = SearchService.search_products(words_list, locale, category_id)
        except HttpError:
            raise
        except Exception as e:
            raise HttpError(500, f"Search failed: {str(e)}")

        if not products:
            return []

        return [product.to_json_single(details_map[product]) for product in products]

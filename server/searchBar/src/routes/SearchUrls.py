from ninja import Router
from ninja.errors import HttpError
from shop.models import Product
from searchBar.src.controllers.SearchControl import SearchControl

router = Router()


@router.get("")
def search_products(
    request,
    locale: str = "en",
    category_id: int | None = None,
    words: list[str] | None = None,
) -> list[Product] | HttpError:
    return SearchControl.search_products(request, locale, category_id, words)

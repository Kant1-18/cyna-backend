from ninja import Router
from ninja.errors import HttpError
from shop.models import Product
from searchBar.src.controllers.SearchControl import SearchControl
from ninja     import Schema, Query

router = Router()

class SearchQuerySchema(Schema):
    locale: str = "en"
    category_id: int = None
    q: str = None

@router.get("")
def search_products(
    request,
    params: Query[SearchQuerySchema],
) -> list[Product] | HttpError:
    return SearchControl.search_products(params.q, params.locale, params.category_id)

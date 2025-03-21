from shop.src.data.models.Discount import Discount
from shop.src.services.DiscountService import DiscountService
from shop.src.services.ProductService import ProductService
from users.src.services.AuthService import AuthService
from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos


class DiscountControl:
    @staticmethod
    def add(request, data) -> Discount | None:
        if AuthService.isAdmin(request):

            if not CheckInfos.is_valid_id(data.productId):
                raise HttpError(400, "Invalid id for product")

            if not CheckInfos.is_percentage(data.percentage):
                raise HttpError(400, "Invalid percentage")

            if not CheckInfos.is_valid_date(data.endDate):
                raise HttpError(400, "Invalid date")

            discount = DiscountService.add(
                data.productId, data.percentage, data.endDate
            )
            if discount:
                return discount.to_json()
            else:
                raise HttpError(500, "Error when adding discount")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def get(id: int) -> Discount | None:
        if not CheckInfos.is_valid_id(id):
            raise HttpError(400, "Invalid id")
        discount = DiscountService.get(id)
        if discount:
            return discount.to_json()
        else:
            raise HttpError(404, "Discount not found")

    @staticmethod
    def get_active_by_product(product_id: int) -> Discount | None:
        if not CheckInfos.is_valid_id(product_id):
            raise HttpError(400, "Invalid id")
        discount = DiscountService.get_active_by_product(product_id)
        if discount:
            return discount.to_json()
        else:
            raise HttpError(404, "No dicount found for the product")

    @staticmethod
    def get_all() -> list[Discount] | None:
        discounts = DiscountService.get_all()
        if discounts:
            return [discount.to_json() for discount in discounts]
        else:
            raise HttpError(404, "No Discount found")

    @staticmethod
    def get_all_active() -> list[Discount] | None:
        discounts = DiscountService.get_all_active()
        if discounts:
            return [discount.to_json() for discount in discounts]
        else:
            raise HttpError(404, "No active Discount found")

    @staticmethod
    def update(request, data) -> Discount | None:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_id(data.id):
                raise HttpError(400, "Invalid id")

            if not CheckInfos.is_percentage(data.percentage):
                raise HttpError(400, "Invalid percentage")

            if not CheckInfos.is_valid_date(data.endDate):
                raise HttpError(400, "Invalid date")

            discount = DiscountService.update(data.id, data.percentage, data.endDate)
            if discount:
                return discount.to_json()
            else:
                raise HttpError(500, "Error when updating discount")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def delete(request, id: int) -> bool:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_id(id):
                raise HttpError(400, "Invalid id")
            if DiscountService.delete(id):
                return True
            else:
                raise HttpError(500, "Error when deleting discount")
        else:
            raise HttpError(403, "Unauthorized")

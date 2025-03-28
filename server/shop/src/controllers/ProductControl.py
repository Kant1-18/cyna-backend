from shop.src.data.models.Product import Product
from shop.src.services.ProductService import ProductService
from users.src.services.AuthService import AuthService
from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos
from shop.src.services.CategoryService import CategoryService


class ProductControl:

    @staticmethod
    def add(request, data) -> Product | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_string(data.name):
                raise HttpError(400, "Invalid name")

            if not CheckInfos.is_valid_string(data.description):
                raise HttpError(400, "Invalid description")

            if not CheckInfos.is_valid_price(data.price):
                raise HttpError(400, "Invalid price")

            if not CheckInfos.is_status_product(data.status):
                raise HttpError(400, "Invalid status")

            if not CheckInfos.is_valid_id(data.categoryId):
                raise HttpError(400, "Invalid id for category")

            if not CheckInfos.is_valid_image_format(data.image):
                raise HttpError(400, "Unsupported image format")

            product = ProductService.add(
                data.name,
                data.description,
                data.price,
                data.status,
                data.categoryId,
                data.image,
            )
            if product:
                return product.to_json()
            else:
                raise HttpError(500, "Error when adding product")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def get(id: int) -> Product | HttpError:
        if not CheckInfos.is_valid_id(id):
            raise HttpError(400, "Invalid id")
        product = ProductService.get(id)
        if product:
            return product.to_json()
        else:
            raise HttpError(404, "Product not found")

    @staticmethod
    def get_all() -> list[Product] | HttpError:
        products = ProductService.get_all()
        if products:
            return [product.to_json() for product in products]
        else:
            raise HttpError(404, "Products not found")

    @staticmethod
    def get_all_by_category(category_id: int) -> list[Product] | HttpError:
        if not CategoryService.is_category_exist(category_id):
            raise HttpError(404, "Category not found")

        products = ProductService.get_by_category(category_id)
        if products:
            return [product.to_json() for product in products]
        else:
            raise HttpError(404, "Products not found for the category")

    @staticmethod
    def update(request, data) -> Product | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_id(data.id):
                raise HttpError(400, "Invalid id")

            if not CheckInfos.is_valid_string(data.name):
                raise HttpError(400, "Invalid string for name")

            if not CheckInfos.is_valid_string(data.description):
                raise HttpError(400, "Invalid string for description")

            if not CheckInfos.is_valid_price(data.price):
                raise HttpError(400, "Invalid price")

            if not CheckInfos.is_status_product(data.status):
                raise HttpError(400, "Invalid status")

            if not CheckInfos.is_valid_id(data.categoryId):
                raise HttpError(400, "Invalid id for category")

            if not CheckInfos.is_valid_string(data.image):
                raise HttpError(400, "Invalid string for image's url")

            product = ProductService.update(
                data.id,
                data.name,
                data.description,
                data.price,
                data.status,
                data.categoryId,
                data.image,
            )
            if product:
                return product.to_json()
            else:
                raise HttpError(500, "Error when updating product")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def update_image(request, data) -> bool | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_id(data.id):
                raise HttpError(400, "Invalid id")
            if not CheckInfos.is_valid_image_format(data.image):
                raise HttpError(400, "Unsupported image format")

            if ProductService.update_image(data.id, data.image):
                return True
            else:
                raise HttpError(500, "Error when updating product image")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def delete(request, id: int) -> bool | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_id(id):
                raise HttpError(400, "Invalid id")
            if ProductService.delete(id):
                return True
            else:
                raise HttpError(500, "Error when deleting product")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def get_all_with_discounts() -> list | HttpError:
        discounts, products = ProductService.get_all_with_discounts()
        if discounts is None and products is None:
            raise HttpError(500, "Error when getting all products")
        if discounts is not None and products is not None:
            return {
                "discounts": [discount.to_json() for discount in discounts],
                "products": [product.to_json() for product in products],
            }
        else:
            return {
                "discounts": [],
                "products": [product.to_json() for product in products],
            }

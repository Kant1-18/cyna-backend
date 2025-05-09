from shop.src.data.models.Product import Product
from shop.src.data.models.ProductDetails import ProductDetails as Details
from shop.src.services.ProductService import ProductService
from users.src.services.AuthService import AuthService
from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos
from shop.src.services.CategoryService import CategoryService


class ProductControl:

    ###########################################################################
    # ADD
    ###########################################################################

    @staticmethod
    def add_product(request, data) -> Product | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data["categoryId"]):
                raise HttpError(400, "Invalid id for category")

            if not CheckInfos.is_valid_string(data["name"]):
                raise HttpError(400, "Invalid name")

            if not CheckInfos.is_type_product(data["type"]):
                raise HttpError(400, "Invalid type")

            if not CheckInfos.is_status_product(data["status"]):
                raise HttpError(400, "Invalid status")

            if not CheckInfos.is_positive_int(data["price"]):
                raise HttpError(400, "Invalid price")

            if not data["discountOrder"] >= 0:
                raise HttpError(400, "Invalid discountOrder")

            if not CheckInfos.is_percentage(data["discountPercentage"]):
                raise HttpError(400, "Invalid discountPercentage")

            if not CheckInfos.is_valid_image_format(data["image1"]):
                raise HttpError(400, "Unsupported image format")

            if not CheckInfos.is_valid_image_format(data["image2"]):
                raise HttpError(400, "Unsupported image format")

            if not CheckInfos.is_valid_image_format(data["image3"]):
                raise HttpError(400, "Unsupported image format")

            product = ProductService.add_product(
                data["categoryId"],
                data["name"],
                data["type"],
                data["status"],
                data["price"],
                data["discountOrder"],
                data["discountPercentage"],
                data["image1"],
                data["image2"],
                data["image3"],
            )
            if product:
                return product.to_json_all()
            else:
                raise HttpError(500, "Error when adding product")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def add_product_details(request, data) -> Details | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data.productId):
                raise HttpError(400, "Invalid id for product")

            if not CheckInfos.is_valid_locale(data.locale):
                raise HttpError(400, "Invalid locale")

            if ProductService.is_product_exist(data.productId, data.locale):
                raise HttpError(409, "locale already exists for this product")

            if not CheckInfos.is_valid_string(data.descriptionTitle):
                raise HttpError(400, "Invalid description_title")

            if not CheckInfos.is_valid_string(data.descriptionText):
                raise HttpError(400, "Invalid description_text")

            if not CheckInfos.is_list_of_str_dicts(data.benefits):
                raise HttpError(400, "Invalid benefits")

            if not CheckInfos.is_list_of_str_dicts(data.specifications):
                raise HttpError(400, "Invalid specifications")

            if not CheckInfos.is_list_of_str_dicts(data.functionalities):
                raise HttpError(400, "Invalid functionalities")

            details = ProductService.add_product_details(
                data.productId,
                data.locale,
                data.descriptionTitle,
                data.descriptionText,
                data.benefits,
                data.functionalities,
                data.specifications,
            )
            if details:
                return details.to_json()
            else:
                raise HttpError(500, "Error when adding product details")
        else:
            raise HttpError(403, "Unauthorized")

    ###########################################################################
    # GET
    ###########################################################################

    @staticmethod
    def get_by_id(id: int) -> Product | HttpError:
        if not CheckInfos.is_positive_int(id):
            raise HttpError(400, "Invalid id")

        product = ProductService.get(id)
        if product:
            return product.to_json_all()
        else:
            raise HttpError(404, "Product not found")

    @staticmethod
    def get_by_id_and_locale(id: int, locale: str) -> Product | HttpError:
        if not CheckInfos.is_positive_int(id):
            raise HttpError(400, "Invalid id")

        if not CheckInfos.is_valid_locale(locale):
            raise HttpError(400, "Invalid locale")

        product, details = ProductService.get_by_locale(id, locale)
        if product and details:
            return product.to_json(details)
        else:
            raise HttpError(404, "Product not found")

    @staticmethod
    def get_all() -> list[Product] | HttpError:
        products = ProductService.get_all()
        if products:
            return [product.to_json_all() for product in products]
        else:
            raise HttpError(404, "No products found")

    @staticmethod
    def get_all_by_locale(locale: str) -> list[Product] | HttpError:
        if not CheckInfos.is_valid_locale(locale):
            raise HttpError(400, "Invalid locale")

        products, details = ProductService.get_all_by_locale(locale)
        if products:
            return [product.to_json(details[product]) for product in products]
        else:
            raise HttpError(404, "No products found")

    @staticmethod
    def get_all_by_category_and_locale(
        category_id: int, locale: str
    ) -> list[Product] | HttpError:
        if not CategoryService.is_category_exist(category_id):
            raise HttpError(400, "Invalid category id")
        if not CheckInfos.is_valid_locale(locale):
            raise HttpError(400, "Invalid locale")

        products, details = ProductService.get_all_by_category_and_locale(
            category_id, locale
        )
        if products:
            return [product.to_json(details[product]) for product in products]
        else:
            raise HttpError(404, "No products found")

    ###########################################################################
    # UPDATE
    ###########################################################################

    @staticmethod
    def update(request, data) -> Product | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data.id):
                raise HttpError(400, "Invalid id")

            if not CategoryService.is_category_exist(data.categoryId):
                raise HttpError(400, "Invalid id for category")

            if not CheckInfos.is_valid_string(data.name):
                raise HttpError(400, "Invalid string for name")

            if not CheckInfos.is_type_product(data.type):
                raise HttpError(400, "Invalid type")

            if not CheckInfos.is_status_product(data.status):
                raise HttpError(400, "Invalid string for description")

            if not CheckInfos.is_positive_int(data.price):
                raise HttpError(400, "Invalid price")

            if data.discountPercentage != None:
                if not CheckInfos.is_positive_int(data.discountOrder):
                    raise HttpError(400, "Invalid discountOrder")

            if data.discountPercentage != None:
                if not CheckInfos.is_percentage(data.discountPercentage):
                    raise HttpError(400, "Invalid discountPercentage")

            product = ProductService.update_product(
                data.id,
                data.categoryId,
                data.name,
                data.type,
                data.status,
                data.price,
                data.discountOrder,
                data.discountPercentage,
            )
            if product:
                return product.to_json_admin()
            else:
                raise HttpError(500, "Error when updating product")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def update_image1(request, data) -> bool | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data["id"]):
                raise HttpError(400, "Invalid id")
            if not CheckInfos.is_valid_image_format(data["image"]):
                raise HttpError(400, "Unsupported image format")

            if ProductService.update_image(data["id"], data["image"]):
                return True
            else:
                raise HttpError(500, "Error when updating product image")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def update_image2(request, data) -> bool | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data["id"]):
                raise HttpError(400, "Invalid id")
            if not CheckInfos.is_valid_image_format(data["image"]):
                raise HttpError(400, "Unsupported image format")

            if ProductService.update_image2(data["id"], data["image"]):
                return True
            else:
                raise HttpError(500, "Error when updating product image")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def update_image3(request, data) -> bool | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data["id"]):
                raise HttpError(400, "Invalid id")
            if not CheckInfos.is_valid_image_format(data["image"]):
                raise HttpError(400, "Unsupported image format")

            if ProductService.update_image3(data["id"], data["image"]):
                return True
            else:
                raise HttpError(500, "Error when updating product image")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def update_details(request, data) -> Details | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data.id):
                raise HttpError(400, "Invalid id")

            if not CheckInfos.is_valid_string(data.descriptionTitle):
                raise HttpError(400, "Invalid string for description title")

            if not CheckInfos.is_valid_string(data.descriptionText):
                raise HttpError(400, "Invalid string for description text")

            details = ProductService.update_details(
                data.id,
                data.descriptionTitle,
                data.descriptionText,
                data.benefits,
                data.functionalities,
                data.specifications,
            )
            if details:
                return details.to_json()
            else:
                raise HttpError(500, "Error when updating product details")
        else:
            raise HttpError(403, "Unauthorized")

    ###########################################################################
    # delete
    ###########################################################################

    @staticmethod
    def delete_by_id(request, id: int) -> bool | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(id):
                raise HttpError(400, "Invalid id")
            if ProductService.delete(id):
                return True
            else:
                raise HttpError(500, "Error when deleting product")
        else:
            raise HttpError(403, "Unauthorized")

    @staticmethod
    def delete_by_id_details(request, id: int) -> bool | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(id):
                raise HttpError(400, "Invalid id")
            if ProductService.delete_details(id):
                return True
            else:
                raise HttpError(500, "Error when deleting product details")
        else:
            raise HttpError(403, "Unauthorized")

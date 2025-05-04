from ninja.errors import HttpError
from shop.src.data.models.Category import Category
from shop.src.services.CategoryService import CategoryService
from users.src.services.AuthService import AuthService
from utils.CheckInfos import CheckInfos


class CategoryControl:

    @staticmethod
    def add(request, data) -> Category | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_string(data.globalName):
                raise HttpError(400, "Invalid string for name")

            category = CategoryService.add(data.globalName)
            if category:
                return category.to_json()
            else:
                raise HttpError(500, "An error occurred while creating the category")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def add_locale(request, data) -> Category | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data.id):
                raise HttpError(400, "Invalid id")

            if not CheckInfos.is_valid_string(data.locale):
                raise HttpError(400, "Invalid string for locale")

            if not CheckInfos.is_valid_string(data.name):
                raise HttpError(400, "Invalid string for name")

            category = CategoryService.add_locale(data.id, data.locale, data.name)
            if category:
                return category.to_json(locale=data.locale)
            else:
                raise HttpError(500, "An error occurred while creating the category")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def get(id: int, locale: str) -> Category | HttpError:
        if not CheckInfos.is_positive_int(id):
            raise HttpError(400, "Invalid id")
        category = CategoryService.get(id)
        return (
            category.to_json(locale=locale)
            if category
            else HttpError(404, "Category not found")
        )

    @staticmethod
    def get_by_global_name(global_name: str) -> Category | HttpError:
        if not CheckInfos.is_valid_string(global_name):
            raise HttpError(400, "Invalid string for name")
        category = CategoryService.get_by_global_name(global_name)
        return category.to_json() if category else HttpError(404, "Category not found")

    @staticmethod
    def get_all() -> list[Category] | HttpError:
        categories = CategoryService.get_all()
        if categories:
            return [category.to_json() for category in categories]
        else:
            raise HttpError(404, "No categories found")

    @staticmethod
    def get_all_locales() -> list[Category] | HttpError:
        categories = CategoryService.get_all()
        if categories:
            return [category.to_json_all_locales() for category in categories]
        else:
            raise HttpError(404, "No Categories found")

    @staticmethod
    def update(request, data) -> Category | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data.id):
                raise HttpError(400, "Invalid id")

            if not CheckInfos.is_valid_string(data.globalName):
                raise HttpError(400, "Invalid string for name")

            category = CategoryService.update(data.id, data.gobalName)
            if category:
                return category.to_json()
            else:
                raise HttpError(500, "An error occurred while updating the category")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def update_locale(request, data) -> Category | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(data.id):
                raise HttpError(400, "Invalid id")

            if not CheckInfos.is_valid_string(data.name):
                raise HttpError(400, "Invalid string for name")

            if not CheckInfos.is_valid_locale(data.locale):
                raise HttpError(400, "Invalid locale")

            category_locale = CategoryService.update_locale(
                data.id, data.locale, data.name
            )
            if category_locale:
                return category_locale.to_json()
            else:
                raise HttpError(500, "An error occurred while updating the category")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def delete(request, id: int) -> bool:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(id):
                raise HttpError(400, "Invalid id")

            result = CategoryService.delete(id)
            if result:
                return True
            else:
                raise HttpError(500, "An error occurred while deleting the category")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def delete_locale(request, locale_id: int) -> bool:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_positive_int(locale_id):
                raise HttpError(400, "Invalid locale id")

            result = CategoryService.delete_locale(locale_id)
            if result:
                return True
            else:
                raise HttpError(500, "An error occurred while deleting the category")
        else:
            raise HttpError(403, "Forbidden")

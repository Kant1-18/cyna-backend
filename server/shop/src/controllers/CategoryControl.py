from ninja.errors import HttpError
from shop.src.data.models.Category import Category
from shop.src.services.CategoryService import CategoryService
from users.src.services.AuthService import AuthService
from utils.CheckInfos import CheckInfos


class CategoryControl:

    @staticmethod
    def add(request, data) -> Category | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_string(data.name):
                raise HttpError(400, "Invalid string for name")

            category = CategoryService.add(data.name)
            if category:
                return category.to_json()
            else:
                raise HttpError(500, "An error occurred while creating the category")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def get(id: int) -> Category | HttpError:
        if not CheckInfos.is_valid_id(id):
            raise HttpError(400, "Invalid id")
        category = CategoryService.get(id)
        return category.to_json() if category else HttpError(404, "Category not found")

    @staticmethod
    def get_by_name(name: str) -> Category | HttpError:
        if not CheckInfos.is_valid_string(name):
            raise HttpError(400, "Invalid string for name")
        category = CategoryService.get_by_name(name)
        return category.to_json() if category else HttpError(404, "Category not found")

    @staticmethod
    def get_all() -> list[Category] | HttpError:
        categories = CategoryService.get_all()
        if categories:
            return [category.to_json() for category in categories]
        else:
            raise HttpError(404, "No categories found")

    @staticmethod
    def update(request, data) -> Category | HttpError:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_id(data.id):
                raise HttpError(400, "Invalid id")

            if not CheckInfos.is_valid_string(data.name):
                raise HttpError(400, "Invalid string for name")

            category = CategoryService.update(data.id, data.name)
            if category:
                return category.to_json()
            else:
                raise HttpError(500, "An error occurred while updating the category")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def delete(request, id: int) -> bool:
        if AuthService.isAdmin(request):
            if not CheckInfos.is_valid_id(id):
                raise HttpError(400, "Invalid id")

            result = CategoryService.delete(id)
            if result:
                return True
            else:
                raise HttpError(500, "An error occurred while deleting the category")
        else:
            raise HttpError(403, "Forbidden")

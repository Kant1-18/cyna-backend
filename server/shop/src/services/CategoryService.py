from shop.src.data.models.Category import Category
from shop.src.data.repositories.CategoryRepo import CategoryRepo


class CategoryService:

    @staticmethod
    def add(global_name: str) -> Category | None:
        return CategoryRepo.add(global_name)

    @staticmethod
    def add_locale(id: int, locale: str, name: str) -> Category | None:
        category = CategoryRepo.get(id)
        if category:
            return CategoryRepo.add_locale(category, locale, name)
        return None

    @staticmethod
    def get(id: int) -> Category | None:
        return CategoryRepo.get(id)

    @staticmethod
    def get_by_global_name(global_name: str) -> Category | None:
        return CategoryRepo.get_by_name(global_name)

    @staticmethod
    def get_all() -> list[Category] | None:
        return CategoryRepo.get_all()

    @staticmethod
    def update(id: int, globalName: str) -> Category | None:
        return CategoryRepo.update(id, globalName)

    @staticmethod
    def update_locale(id: int, locale: str, name: str) -> Category | None:
        return CategoryRepo.update_locale(id, locale, name)

    @staticmethod
    def delete(id: int) -> bool:
        return CategoryRepo.delete(id)

    @staticmethod
    def delete_locale(locale_id: int) -> bool:
        return CategoryRepo.delete_locale(locale_id)

    @staticmethod
    def is_category_exist(id: int) -> bool:
        return CategoryRepo.is_category_exist(id)

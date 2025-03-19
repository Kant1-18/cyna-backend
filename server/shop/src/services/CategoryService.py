from typing import Optional, List
from shop.src.data.models.Category import Category
from shop.src.data.repositories.CategoryRepo import CategoryRepo


class CategoryService:

    @staticmethod
    def add(name: str) -> Optional[Category]:
        return CategoryRepo.add(name)

    @staticmethod
    def get(id: int) -> Optional[Category]:
        return CategoryRepo.get(id)

    @staticmethod
    def get_by_name(name: str) -> Optional[Category]:
        return CategoryRepo.get_by_name(name)

    @staticmethod
    def get_all() -> Optional[List[Category]]:
        return CategoryRepo.get_all()

    @staticmethod
    def update(id: int, name: str) -> Optional[Category]:
        return CategoryRepo.update(id, name)

    @staticmethod
    def delete(id: int) -> bool:
        return CategoryRepo.delete(id)

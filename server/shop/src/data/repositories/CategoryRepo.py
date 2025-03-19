from typing import Optional, List
from shop.src.data.models.Category import Category

class CategoryRepo:
    
    @staticmethod
    def add(name: str) -> Category:
        try:
            category = Category.objects.create(name=name)
            if category:
                return category
        except Exception as e:
            print(e)
            
        return None
    
    @staticmethod
    def get(id: int) -> Optional[Category]:
        try:
            category = Category.objects.get(id=id)
            if category:
                return category
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def get_by_name(name: str) -> Optional[Category]:
        try:
            category = Category.objects.get(name=name)
            if category:
                return category
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def get_all() -> Optional[List[Category]]:
        try:
            categories = Category.objects.all()
            if categories:
                return categories
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def update(id: int, name: str) -> Optional[Category]:
        try:
            category = Category.objects.get(id=id)
            if category:
                category.name = name
                category.save()
                return category
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def delete(id: int) -> bool:
        try:
            category = Category.objects.get(id=id)
            if category:
                category.delete()
        except Exception as e:
            print(e)

        return True if not Category.objects.filter(id=id).exists() else False

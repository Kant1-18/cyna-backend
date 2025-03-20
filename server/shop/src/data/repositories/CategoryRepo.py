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
    def get(id: int) -> (Category | None):
        try:
            category = Category.objects.get(id=id)
            if category:
                return category
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_name(name: str) -> (Category | None):
        try:
            category = Category.objects.get(name=name)
            if category:
                return category
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> (list[Category] | None):
        try:
            categories = Category.objects.all()
            if categories:
                return categories
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(id: int, name: str) -> (Category | None):
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
                return True
        except Exception as e:
            print(e)

        return False

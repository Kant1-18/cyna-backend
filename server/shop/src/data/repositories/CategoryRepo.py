from shop.models import Category
from shop.models import CategoryLocale


class CategoryRepo:

    @staticmethod
    def add(global_name: str) -> Category:
        try:
            category = Category.objects.create(global_name=global_name)
            if category:
                category_locale = CategoryLocale.objects.create(
                    category=category, locale="en", name=global_name
                )
                if category_locale:
                    return category
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def add_locale(category: Category, locale: str, name: str) -> Category:
        try:
            category_locale = CategoryLocale.objects.create(
                category=category, locale=locale, name=name
            )
            if category_locale:
                return category
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def get(id: int) -> Category | None:
        try:
            category = Category.objects.get(id=id)
            if category:
                return category
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_name(name: str) -> Category | None:
        try:
            category = Category.objects.get(name=name)
            if category:
                return category
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> list[Category] | None:
        try:
            categories = Category.objects.all()
            if categories:
                return categories
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(id: int, name: str) -> Category | None:
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
    def update_locale(locale_id: int, locale: str, name: str) -> Category | None:
        try:
            locale = CategoryLocale.objects.get(id=locale_id)
            if locale:
                locale.locale = locale
                locale.name = name
                locale.save()
                return locale
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

    @staticmethod
    def delete_locale(locale_id: int) -> bool:
        try:
            category_locale = CategoryLocale.objects.get(id=locale_id)
            if category_locale:
                category_locale.delete()
                return True
        except Exception as e:
            print(e)

        return False

    @staticmethod
    def is_category_exist(id: int) -> bool:
        return Category.objects.filter(id=id).exists()

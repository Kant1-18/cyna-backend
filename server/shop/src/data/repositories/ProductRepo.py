from shop.src.data.repositories.CategoryRepo import CategoryRepo
from shop.src.data.models.Product import Product
from shop.src.data.models.Category import Category


class ProductRepo:

    @staticmethod
    def add(
        name: str,
        descripton: str,
        price: int,
        status: int,
        category: Category,
        image: str,
    ) -> Product | None:
        try:
            product = Product.objects.create(
                name=name,
                description=descripton,
                price=price,
                status=status,
                category=category,
                image=image,
                top_order=0,
            )
            if product:
                return product
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get(id: int) -> Product | None:
        try:
            product = Product.objects.get(id=id)
            if product:
                return product
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> list[Product] | None:
        try:
            products = Product.objects.all()
            if products:
                return products
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_by_category(category: Category) -> list[Product] | None:
        try:
            products = Product.objects.filter(category=category)
            if products:
                return products
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(
        id: int,
        name: str,
        descripton: str,
        price: int,
        status: int,
        category: Category,
        image: str,
    ) -> Product | None:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.name = name
                product.description = descripton
                product.price = price
                product.status = status
                product.category = category
                product.image = image
                product.save()
                return product
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_top(id: int, top_order: int) -> Product | None:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.top_order = top_order
                product.save()
                return product
        except Exception as e:
            print(e)

    @staticmethod
    def delete(id: int) -> bool:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.delete()
                return True
        except Exception as e:
            print(e)

        return False

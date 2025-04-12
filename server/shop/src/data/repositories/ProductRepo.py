from shop.src.data.repositories.CategoryRepo import CategoryRepo
from shop.src.data.models.Product import Product
from shop.src.data.models.Category import Category


class ProductRepo:

    @staticmethod
    def add(
        category: Category,
        status: int,
        base_price: int,
        price: int,
        discount_order: int,
        discount_percentage: int,
        image1: str,
        image2: str,
        image3: str,
    ) -> Product | None:
        try:
            product = Product.objects.create(
                category=category,
                status=status,
                base_price=base_price,
                price=price,
                discount_order=discount_order,
                discount_percentage=discount_percentage,
                image1=image1,
                image2=image2,
                image3=image3,
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
        category: Category,
        status: int,
        base_price: int,
        discount_order: int,
        discount_percentage: int,
    ) -> Product | None:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.category = category
                product.status = status
                product.base_price = base_price
                product.discount_order = discount_order
                product.discount_percentage = discount_percentage
                product.save()
                return product
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_image1(id: int, image_url: str) -> bool:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.image1 = image_url
                product.save()
                return True
        except Exception as e:
            print(e)

        return False

    @staticmethod
    def update_image2(id: int, image_url: str) -> bool:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.image2 = image_url
                product.save()
                return True
        except Exception as e:
            print(e)

        return False

    @staticmethod
    def update_image3(id: int, image_url: str) -> bool:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.image3 = image_url
                product.save()
                return True
        except Exception as e:
            print(e)

        return False

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

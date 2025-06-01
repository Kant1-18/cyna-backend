from shop.src.data.repositories.CategoryRepo import CategoryRepo
from shop.src.data.models.Product import Product
from shop.src.data.models.Category import Category
from shop.src.data.models.OrderItem import OrderItem
from django.db.models import Sum


class ProductRepo:

    @staticmethod
    def add(
        category: Category,
        name: str,
        type: int,
        status: int,
        base_price: int,
        discount_order: int,
        discount_percentage: int,
        image1: str,
        image2: str,
        image3: str,
        stripe_id: str,
        stripe_monthly_price_id: str,
        stripe_yearly_price_id: str,
    ) -> Product | None:
        try:
            product = Product.objects.create(
                category=category,
                name=name,
                type=type,
                status=status,
                base_price=base_price,
                price=(base_price * (1 - discount_percentage / 100)),
                discount_order=discount_order,
                discount_percentage=discount_percentage,
                image1=image1,
                image2=image2,
                image3=image3,
                stripe_id=stripe_id,
                stripe_monthly_price_id=stripe_monthly_price_id,
                stripe_yearly_price_id=stripe_yearly_price_id,
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
    def get_best_seller() -> Product | None:
        try:
            quantity_sold = OrderItem.objects.filter(order__status=5).values("product").annotate(total_sold=Sum("quantity")).order_by("-total_sold")
            if not quantity_sold:
                return None
            
            top = quantity_sold[0]
            product_id = top["product"]
            total_sold = top["total_sold"] or 0

            return { "product_id": product_id, "total_sold": total_sold  }
        except Exception as e:
            print(e)

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
        product: Product,
        category: Category,
        name: str,
        type: int,
        status: int,
        base_price: int,
        discount_order: int,
        discount_percentage: int,
        stripe_monthly_price_id: str,
        stripe_yearly_price_id: str,
    ) -> Product | None:
        try:
            if product:
                product.category = category
                product.name = name
                product.type = type
                product.status = status
                product.base_price = base_price
                product.price = base_price * (1 - discount_percentage / 100)
                product.discount_order = discount_order
                product.discount_percentage = discount_percentage
                product.stripe_monthly_price_id = stripe_monthly_price_id
                product.stripe_yearly_price_id = stripe_yearly_price_id
                product.save()
                return product
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_image1(id: int, image_url: str) -> Product | None:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.image1 = image_url
                product.save()
                return product
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_image2(id: int, image_url: str) -> Product | None:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.image2 = image_url
                product.save()
                return product
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_image3(id: int, image_url: str) -> Product | None:
        try:
            product = Product.objects.get(id=id)
            if product:
                product.image3 = image_url
                product.save()
                return product
        except Exception as e:
            print(e)
            return None

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

from typing import Optional, List
from shop.src.data.repositories.CategoryRepo import CategoryRepo
from shop.src.data.models.Product import Product

class ProductRepo:
    
    @staticmethod
    def add(name: str, descripton: str, price: int, status: int, category_id: int, image: str, discount: int, discount_order: int, top_order: int):
        try:
            category = CategoryRepo.get(category_id)
            if category:
                product = Product.objects.create(
                    name=name,
                    description=descripton,
                    price=price,
                    status=status,
                    category=category,
                    image=image,
                    discount=discount,
                    discount_order=discount_order,
                    top_order=top_order
                )
                if product:
                    return product
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def get(id: int) -> Optional[Product]:
        try:
            product = Product.objects.get(id=id)
            if product:
                return product
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def get_all() -> Optional[List[Product]]:
        try:
            products = Product.objects.all()
            if products:
                return products
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def get_all_by_category(category_id: int) -> Optional[List[Product]]:
        try:
            category = CategoryRepo.get(category_id)
            if category:
                products = Product.objects.filter(category=category)
                if products:
                    return products
        except Exception as e:
            print(e)

        return None
    
    @staticmethod
    def update(id: int, name: str, descripton: str, price: int, status: int, category_id: int, image: str, discount: int, discount_order: int, top_order: int):
        try:
            category = CategoryRepo.get(category_id)
            if category:
                product = Product.objects.get(id=id)
                if product:
                    product.name = name
                    product.description = descripton
                    product.price = price
                    product.status = status
                    product.category = category
                    product.image = image
                    product.discount = discount
                    product.discount_order = discount_order
                    product.top_order = top_order
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
        except Exception as e:
            print(e)

        return True if not Product.objects.filter(id=id).exists() else False

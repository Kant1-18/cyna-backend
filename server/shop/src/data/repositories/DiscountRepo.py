from shop.src.data.models.Discount import Discount
from shop.src.data.models.Product import Product
from shop.src.services.ProductService import ProductService
import datetime

class DiscountRepo:
    
    @staticmethod
    def add(product: Product, percentage: int, end_date: str):
        try:
            discount_price = product.price * percentage / 100
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            dicount = Discount.objects.create(product=product, percentage=percentage, discount_price=discount_price, end_date=end_date)
            if dicount:
                return dicount
        except Exception as e:
            print(e)
            
        return None
    
    
    @staticmethod
    def get(id: int):
        try:
            discount = Discount.objects.get(id=id)
            if discount:
                return discount
        except Exception as e:
            print(e)
            
        return None
    
    
    @staticmethod
    def get_active_by_product(product: Product):
        try:
            discounts = Discount.objects.filter(product=product, end_date__gte=datetime.datetime.now())
            if discounts:
                return discounts
        except Exception as e:
            print(e)
            
        return None
    
    
    @staticmethod
    def get_all():
        try:
            discounts = Discount.objects.all()
            if discounts:
                return discounts
        except Exception as e:
            print(e)
            
        return None
    
    
    @staticmethod
    def get_all_active():
        try:
            discounts = Discount.objects.filter(end_date__gte=datetime.datetime.now())
            if discounts:
                return discounts
        except Exception as e:
            print(e)
            
        return None
    
    
    @staticmethod
    def update(id: int, percentage: int, end_date: str):
        try:
            discount = Discount.objects.get(id=id)
            if discount:
                discount.percentage = percentage
                discount.end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y")
                discount.save()
                return discount
        except Exception as e:
            print(e)
            
        return None
    
    
    @staticmethod
    def delete(id: int):
        try:
            discount = Discount.objects.get(id=id)
            if discount:
                discount.delete()
                return discount
        except Exception as e:
            print(e)
            
        return None

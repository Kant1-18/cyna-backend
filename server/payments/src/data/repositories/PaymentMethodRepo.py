from payments.models import PaymentMethod


class PaymentMethodRepo:

    @staticmethod
    def add(name: str, stripe_code: str) -> PaymentMethod | None:
        try:
            method = PaymentMethod.objects.create(name=name, stripe_code=stripe_code)
            if method:
                return method
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get(id: int) -> PaymentMethod | None:
        try:
            method = PaymentMethod.objects.get(id=id)
            if method:
                return method
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_name(name: str) -> PaymentMethod | None:
        try:
            method = PaymentMethod.objects.get(name=name)
            if method:
                return method
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all() -> list[PaymentMethod] | None:
        try:
            methods = PaymentMethod.objects.all()
            if methods:
                return methods
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(method_id: int, name: str, stripe_code: str) -> PaymentMethod | None:
        try:
            method = PaymentMethod.objects.get(id=method_id)
            if method:
                method.name = name
                method.stripe_code = stripe_code
                method.save()
                return method
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete(method_id: int) -> bool:
        try:
            method = PaymentMethod.objects.get(id=method_id)
            if method:
                method.delete()
                return True
        except Exception as e:
            print(e)

        return False

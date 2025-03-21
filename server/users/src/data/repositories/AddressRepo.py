from users.src.data.models.User import User
from users.src.data.models.Address import Address


class AddressRepo:

    @staticmethod
    def add(
        user: User,
        type: int,
        street: str,
        number: str,
        complement: str,
        zip_code: str,
        city: str,
        region: str,
        country: str,
    ) -> Address | None:
        try:
            address = Address.objects.create(
                user=user,
                type=type,
                street=street,
                number=number,
                complement=complement,
                zip_code=zip_code,
                city=city,
                region=region,
                country=country,
            )
            if address:
                return address
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get(id: int) -> Address | None:
        try:
            address = Address.objects.get(id=id)
            if address:
                return address
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_all_by_user(user: User) -> list[Address] | None:
        try:
            addresses = Address.objects.filter(user=user)
            if addresses:
                return addresses
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(
        id: int,
        type: int,
        street: str,
        number: str,
        complement: str,
        zip_code: str,
        city: str,
        region: str,
        country: str,
    ) -> Address | None:
        try:
            address = Address.objects.get(id=id)
            if address:
                address.type = type
                address.street = street
                address.number = number
                address.complement = complement
                address.zip_code = zip_code
                address.city = city
                address.region = region
                address.country = country
                address.save()
                return address
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete(id: int) -> bool:
        try:
            address = Address.objects.get(id=id)
            if address:
                address.delete()
                return True
        except Exception as e:
            print(e)

        return False

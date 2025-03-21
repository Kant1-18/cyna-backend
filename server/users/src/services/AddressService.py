from users.src.data.models.User import User
from users.src.data.models.Address import Address
from users.src.data.repositories.AddressRepo import AddressRepo


class AddressService:

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
        return AddressRepo.add(
            user, type, street, number, complement, zip_code, city, region, country
        )

    @staticmethod
    def get(id: int) -> Address | None:
        return AddressRepo.get(id)

    @staticmethod
    def get_all_by_user(user: User) -> list[Address] | None:
        return AddressRepo.get_all_by_user(user)

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
        return AddressRepo.update(
            id, type, street, number, complement, zip_code, city, region, country
        )

    @staticmethod
    def delete(id: int) -> bool:
        return AddressRepo.delete(id)

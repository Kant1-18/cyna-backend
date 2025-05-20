from users.src.data.repositories.UserRepo import UserRepo
from users.src.data.models.User import User
from utils.Stripe import StripeUtils


class UserService:

    @staticmethod
    def add(first_name: str, last_name: str, email: str, password: str) -> User | None:
        try:
            stripe_customer = StripeUtils.create_customer(
                email=email, name=f"{first_name} {last_name}"
            )
            return UserRepo.add(
                first_name,
                last_name,
                email,
                password,
                role=0,
                stripe_id=stripe_customer.id,
            )
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def add_admin(
        first_name: str, last_name: str, email: str, password: str
    ) -> User | None:
        return UserRepo.add(
            first_name, last_name, email, password, role=1, stripe_id=None
        )

    @staticmethod
    def get(id: int) -> User | None:
        return UserRepo.get(id)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return UserRepo.get_by_email(email)

    @staticmethod
    def get_all() -> list[User] | None:
        return UserRepo.get_all()

    @staticmethod
    def get_all_by_role(role: int) -> list[User] | None:
        return UserRepo.get_all_by_role(role)

    @staticmethod
    def update(id: int, first_name: str, last_name: str, email: str) -> User | None:
        return UserRepo.update(id, first_name, last_name, email)

    @staticmethod
    def update_password(id: int, password: str) -> User | None:
        return UserRepo.update_password(id, password)

    @staticmethod
    def delete(id: int) -> bool:
        return UserRepo.delete(id)

    @staticmethod
    def check_password(id: int, password: str) -> bool:
        return UserRepo.check_password(id, password)

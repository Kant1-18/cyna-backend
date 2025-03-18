from users.src.data.repositories.UserRepo import UserRepo
from users.src.data.models.User import User
from typing import Optional, List


class UserService:

    @staticmethod
    def add(first_name: str, last_name: str, email: str, role: int, password: str) -> Optional[User]:
        return UserRepo.add(first_name, last_name, email, role, password)

    @staticmethod
    def get(id: int) -> Optional[User]:
        return UserRepo.get(id)

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return UserRepo.get_by_email(email)

    @staticmethod
    def update(id: int, first_name: str, last_name: str, email: str, role: int) -> Optional[User]:
        return UserRepo.update(id, first_name, last_name, email, role)

    @staticmethod
    def update_password(id: int, password: str) -> Optional[User]:
        return UserRepo.update_password(id, password)

    @staticmethod
    def delete(id: int) -> bool:
        return UserRepo.delete(id)

    @staticmethod
    def check_password(id: int, password: str) -> bool:
        return UserRepo.check_password(id, password)

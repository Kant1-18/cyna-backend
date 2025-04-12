from users.src.services.UserService import UserService
from users.src.services.AuthService import AuthService
from users.src.data.models.User import User
from utils.CheckInfos import CheckInfos
from ninja.errors import HttpError


class UsersControl:

    @staticmethod
    def get(id: int) -> User | HttpError:
        user = UserService.get(id)
        if not user:
            raise HttpError(404, "User not found")
        return user.to_json()

    @staticmethod
    def get_by_email(email: str) -> User | HttpError:
        if not CheckInfos.is_email(email):
            raise HttpError(400, "Invalid email")
        user = UserService.get_by_email(email)
        return user.to_json() if user else HttpError(404, "User not found")

    @staticmethod
    def update(request, data) -> User | HttpError:
        if not CheckInfos.is_valid_string(data.firstName):
            raise HttpError(400, "Invalid firstName")
        if not CheckInfos.is_valid_string(data.lastName):
            raise HttpError(400, "Invalid lastName")
        if not CheckInfos.is_email(data.email):
            raise HttpError(400, "Invalid email")
        if not CheckInfos.is_users_role(data.role):
            raise HttpError(400, "Invalid role")

        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)
        user = UserService.update(
            user.id, data.firstName, data.lastName, data.email, data.role
        )
        return user.to_json() if user else HttpError(500, "An error occurred")

    @staticmethod
    def update_password(request, data) -> User | HttpError:
        if not UserService.check_password(data.id, data.previousPassword):
            raise HttpError(400, "Invalid privious password")

        if not CheckInfos.is_valid_password(
            data.newPassword
        ) or not CheckInfos.is_valid_password(data.confirmNewPassword):
            raise HttpError(400, "Invalid new passwords")

        if not data.newPassword == data.confirmNewPassword:
            raise HttpError(400, "Passwords doesn't match")

        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)
        user = UserService.update_password(user.id, data.newPassword)
        return user.to_json() if user else HttpError(500, "An error occurred")

    @staticmethod
    def delete(id: int) -> bool:
        return UserService.delete(id)

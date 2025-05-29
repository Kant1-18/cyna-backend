from users.src.services.UserService import UserService
from users.src.services.AuthService import AuthService
from users.src.data.models.User import User
from utils.CheckInfos import CheckInfos
from ninja.errors import HttpError
import stripe


class UsersControl:

    @staticmethod
    def add_admin(request, data) -> User | HttpError:
        try:
            if not AuthService.isAdmin(request):
                raise HttpError(403, "Not authorized")
            if not CheckInfos.is_valid_string(data.firstName):
                raise HttpError(400, "Invalid firstName")
            if not CheckInfos.is_valid_string(data.lastName):
                raise HttpError(400, "Invalid lastName")
            if not CheckInfos.is_email(data.email):
                raise HttpError(400, "Invalid email")
            if not CheckInfos.is_valid_password(
                data.password
            ) or not CheckInfos.is_valid_password(data.confirmPassword):
                raise HttpError(400, "Invalid passwords")

            if not data.password == data.confirmPassword:
                raise HttpError(400, "Passwords doesn't match")

            user = UserService.add_admin(
                data.firstName, data.lastName, data.email, data.password
            )
            if user:
                return user.to_json()
        except Exception as e:
            print(e)
            raise HttpError(500, "An error occurred")

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
    def get_all(request, role: int | None) -> list[User] | HttpError:
        if AuthService.isAdmin(request):
            if role is None:
                users = UserService.get_all()
            else:
                users = UserService.get_all_by_role(role)

            if users:
                return [user.to_json() for user in users]
            else:
                raise HttpError(404, "Users not found")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def update(request, data) -> User | HttpError:
        if not CheckInfos.is_valid_string(data.firstName):
            raise HttpError(400, "Invalid firstName")
        if not CheckInfos.is_valid_string(data.lastName):
            raise HttpError(400, "Invalid lastName")
        if not CheckInfos.is_email(data.email):
            raise HttpError(400, "Invalid email")

        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)
        user = UserService.update(user.id, data.firstName, data.lastName, data.email)
        if user.stripe_id:
            try:
                stripe.Customer.modify(id=user.stripe_id, email=data.email, name=f"{data.firstName} {data.lastName}")
            except stripe.error.StripeError as e:
                raise HttpError(400, f"An error occured while updating stripe customer: {e.user_message}")
        return user.to_json() if user else HttpError(500, "An error occurred")

    @staticmethod
    def update_password(request, data) -> User | HttpError:
        token = AuthService.get_token(request)
        user = AuthService.get_user_by_access_token(token)
        if not UserService.check_password(user.id, data.previousPassword):
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

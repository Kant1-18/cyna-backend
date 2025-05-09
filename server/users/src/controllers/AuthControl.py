from users.src.services.UserService import UserService
from utils.CheckInfos import CheckInfos
from ninja.errors import HttpError
from users.src.services.AuthService import AuthService
from ninja.responses import Response
from django.http import JsonResponse


class AuthControl:

    @staticmethod
    def register(data):
        if not CheckInfos.is_valid_string(
            data.firstName
        ) or not CheckInfos.is_valid_string(data.lastName):
            raise HttpError(400, "firstName or lastName invalid")

        if data.password != data.confirmPassword:
            raise HttpError(400, "passwords don't match")

        if not CheckInfos.is_email(data.email):
            raise HttpError(400, "Invalid email")

        if not CheckInfos.is_valid_password(data.password):
            raise HttpError(400, "password invalid")

        if UserService.get_by_email(data.email):
            raise HttpError(409, "email already exists")

        user = UserService.add(data.firstName, data.lastName, data.email, data.password)
        if not user:
            raise HttpError(500, "An error occurred while creating the user")

        return "User created successfully"

    @staticmethod
    def login(data):
        user = UserService.get_by_email(data.email)
        if user and UserService.check_password(user.id, data.password):
            tokens = AuthService.tokens_for_user(user)

            response = JsonResponse(
                {
                    "access": tokens["access"],
                    "user": user.to_json(),
                }
            )

            # Ajout du refresh token dans un cookie HttpOnly sécurisé
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=True,
                samesite="Strict",  # ou 'Lax' selon les besoins
                max_age=7 * 24 * 3600,  # 1 semaine
            )
            return response

        raise HttpError(401, "email or password invalid")

    @staticmethod
    def refresh(request):
        try:
            token = request.COOKIES.get("refresh_token")

            if not token or token.strip() == "":
                raise HttpError(401, "Refresh token missing")

            user = AuthService.get_user_by_refresh_token(token)

            if not user:
                raise HttpError(404, "User not found")

            new_tokens = AuthService.tokens_for_user(user)
            response = JsonResponse({"access": new_tokens["access"]})

            # Réémet le refresh token
            response.set_cookie(
                key="refresh_token",
                value=new_tokens["refresh"],
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=7 * 24 * 3600,
            )
            return response

        except Exception as e:
            print(f"Token refresh error: {e}")
            raise HttpError(401, "Invalid or expired refresh token")

    @staticmethod
    def me(request):
        try:
            token = AuthService.get_token(request)
            user = AuthService.get_user_by_access_token(token)

            if not user:
                raise HttpError(404, "User not found")

            return user.to_json()

        except Exception as e:
            print(f"Token refresh error: {e}")
            raise HttpError(401, "Invalid or expired refresh token")

    @staticmethod
    def logout(request):
        response = JsonResponse({"detail": "Logged out"})
        response.delete_cookie("refresh_token")
        return response

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from users.src.services.UserService import UserService

class AuthService:
    
    @staticmethod
    def get_token(request):
        token = request.headers.get("Authorization").split(" ")[1]
        return token
    
    @staticmethod
    def get_user_with_access_token(token):
        try:
            access = AccessToken(token)
            user_id = access.payload["user_id"]
            return UserService.get(user_id)
        except Exception as e:
            return None

    @staticmethod
    def get_user_with_refresh_token(token):
        try:
            refresh = RefreshToken(token)
            user_id = refresh.payload["user_id"]
            print(user_id)
            return UserService.get(user_id)
        except Exception as e:
            return None

    @staticmethod
    def tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

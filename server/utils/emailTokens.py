from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

VERIFY_SALT = "email-verify"
RESET_SALT = "password-reset"


def generate_token(email: str, salt: str) -> str:
    return serializer.dumps(email, salt=salt)


def verify_token(token: str, salt: str, max_age: int = 3600) -> str:
    try:
        email = serializer.loads(token, salt=salt, max_age=max_age)
        return email
    except SignatureExpired:
        raise ValueError("Token expired")
    except BadSignature:
        raise ValueError("Invalid token")

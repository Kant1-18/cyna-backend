from typing import Optional
from users.src.data.models.User import User
from users.src.data.models.UserCredential import UserCredential
from utils.HashPass import gen_salt, encrypt, check_pass


class UserRepo:

    @staticmethod
    def add(
        first_name: str, last_name: str, email: str, role: int, password: str
    ) -> Optional[User]:
        salt = gen_salt()
        hashed_pass = encrypt(password, salt)
        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,
                role=role,
            )
            if user:
                cred = UserCredential.objects.create(
                    user=user, salt=salt, password=hashed_pass
                )
                if cred:
                    return user
                else:
                    user.delete()
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get(id: int) -> Optional[User]:
        try:
            user = User.objects.get(id=id)
            if user:
                return user
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        try:
            user = User.objects.get(email=email)
            if user:
                return user
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update(
        id: int, first_name: str, last_name: str, email: str, role: int
    ) -> Optional[User]:
        try:
            user = User.objects.get(id=id)
            if user:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                return user
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def update_password(id: int, password: str) -> Optional[User]:
        try:
            user = User.objects.get(id=id)
            cred = UserCredential.objects.get(user=user)
            if user and cred:
                cred.password = encrypt(password, cred.salt)
                cred.save()
                return user
        except Exception as e:
            print(e)

        return None

    @staticmethod
    def delete(id: int) -> bool:
        try:
            user = User.objects.get(id=id)
            if user:
                user.delete()
        except Exception as e:
            print(e)

        return True if not User.objects.filter(id=id).exists() else False

    @staticmethod
    def check_password(id: int, password: str) -> bool:
        try:
            user = User.objects.get(id=id)
            if user:
                cred = UserCredential.objects.get(user=user)
                return check_pass(password, cred.salt, cred.password)
        except Exception as e:
            print(e)

        return False

from typing import Optional, List
from users.src.data.models.User import User
from users.src.data.models.UserCredential import UserCredential
from utils.hashpass import gen_salt, encrypt, check_pass


class UserRepo:

    @staticmethod
    def add(firstName: str, lastName: str, email: str, password: str) -> Optional[User]:
        salt = gen_salt()
        hashedPass = encrypt(password, salt)
        try:
            user = User.objects.create(
                firstName=firstName, lastName=lastName, email=email, username=email
            )
            if user:
                cred = UserCredential.objects.create(
                    user=user, salt=salt, password=hashedPass
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
    def update(id: int, firstName: str, lastName: str, email: str) -> Optional[User]:
        try:
            user = User.objects.get(id=id)
            if user:
                user.firstName = firstName
                user.lastName = lastName
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

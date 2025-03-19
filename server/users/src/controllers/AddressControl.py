from users.src.data.models.User import User
from users.src.data.models.Address import Address
from users.src.services.AddressService import AddressService
from typing import Optional, List
from utils.checkInfos import CheckInfos
from ninja.errors import HttpError
from users.src.services.AuthService import AuthService


class AddressControl:

    @staticmethod
    def add(request, data) -> Optional[Address]:
        try:
            token = AuthService.get_token(request)
            user = AuthService.get_user_by_access_token(token)

            if not user:
                raise HttpError(404, "User not found")

            if not CheckInfos.is_type_address(data.type):
                raise HttpError(400, "Invalid type")

            if not CheckInfos.is_valid_string(data.street):
                raise HttpError(400, "Invalid street")

            if not CheckInfos.is_valid_string(data.number):
                raise HttpError(400, "Invalid number")

            if data.complement:
                if not CheckInfos.is_valid_string(data.complement):
                    raise HttpError(400, "Invalid complement")

            if not CheckInfos.is_valid_string(data.zipCode):
                raise HttpError(400, "Invalid zipCode")

            if not CheckInfos.is_valid_string(data.city):
                raise HttpError(400, "Invalid city")

            if not CheckInfos.is_valid_string(data.region):
                raise HttpError(400, "Invalid region")

            if not CheckInfos.is_valid_string(data.country):
                raise HttpError(400, "Invalid country")

            address = AddressService.add(
                user,
                data.type,
                data.street,
                data.number,
                data.complement,
                data.zipCode,
                data.city,
                data.region,
                data.country,
            )
            if address:
                return address.to_json()
            else:
                raise HttpError(500, "An error occurred")
        except Exception as e:
            print(f"error: {e}")
            raise HttpError(401, "Invalid or expired refresh token")

    @staticmethod
    def get(id: int) -> Optional[Address]:
        address = AddressService.get(id)
        return address.to_json() if address else HttpError(404, "Address not found")

    @staticmethod
    def get_all_by_user(request) -> Optional[List[Address]]:
        try:
            token = AuthService.get_token(request)
            user = AuthService.get_user_by_access_token(token)

            if not user:
                raise HttpError(404, "User not found")

            addresses = AddressService.get_all_by_user(user)
            return (
                [address.to_json() for address in addresses]
                if addresses
                else HttpError(404, "Addresses not found")
            )
        except Exception as e:
            print(f"Token refresh error: {e}")
            raise HttpError(401, "Invalid or expired refresh token")

    @staticmethod
    def update(data) -> Optional[Address]:
        try:
            if not CheckInfos.is_valid_id(data.id):
                raise HttpError(400, "Invalid id")

            if not CheckInfos.is_type_address(data.type):
                raise HttpError(400, "Invalid type")

            if not CheckInfos.is_valid_string(data.street):
                raise HttpError(400, "Invalid string")

            if not CheckInfos.is_valid_string(data.number):
                raise HttpError(400, "Invalid string")

            if not CheckInfos.is_valid_string(data.complement):
                raise HttpError(400, "Invalid string")

            if not CheckInfos.is_valid_string(data.zipCode):
                raise HttpError(400, "Invalid string")

            if not CheckInfos.is_valid_string(data.city):
                raise HttpError(400, "Invalid string")

            if not CheckInfos.is_valid_string(data.region):
                raise HttpError(400, "Invalid string")

            if not CheckInfos.is_valid_string(data.country):
                raise HttpError(400, "Invalid string")

            address = AddressService.update(
                data.id,
                data.type,
                data.street,
                data.number,
                data.complement,
                data.zipCode,
                data.city,
                data.region,
                data.country,
            )
            return address.to_json() if address else HttpError(500, "An error occurred")
        except Exception as e:
            print(f"error: {e}")
            raise HttpError(500, "An error occurred")

    @staticmethod
    def delete(id: int) -> bool:
        return AddressService.delete(id)

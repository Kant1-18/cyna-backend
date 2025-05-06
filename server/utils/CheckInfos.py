import re
from datetime import datetime
import os
from ninja.files import UploadedFile


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

# User Roles
USER_ROLES = [0, 1]

# Types
ADDRESS_TYPES = [0, 1]
PRODUCT_TYPES = [0, 1]
SUBSCRIPTION_TYPES = [0, 1]

# Status
PRODUCT_STATUS = [0, 1]
ORDER_STATUS = [0, 1, 2, 3, 4, 5]
PAYMENT_STATUS = [0, 1, 2, 3, 4]
TICKET_STATUS = [0, 1, 2]


class CheckInfos:

    @staticmethod
    def is_email(email: str) -> bool:
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(email_regex, email))

    @staticmethod
    def is_valid_string(string: str) -> bool:
        if len(string) > 0 and len(string) < 100:
            return True
        else:
            return False

    @staticmethod
    def is_positive_int(id: int) -> bool:
        if id > 0:
            return True
        else:
            return False

    @staticmethod
    def is_valid_price(number: int) -> bool:
        if number > 0 and len(str(number)) >= 4:
            return True
        else:
            return False

    @staticmethod
    def is_percentage(percentage: int) -> bool:
        if percentage >= 0 and percentage <= 100:
            return True
        else:
            return False

    @staticmethod
    def is_valid_password(password: str) -> bool:
        if len(password) < 8:
            return False

        if not re.search(r"\d", password):
            return False

        if not re.search(r"[A-Z]", password):
            return False

        if not re.search(r"[a-z]", password):
            return False

        if not re.search(r"[-!@#$%^&*(),.?\":{}|<>]", password):
            return False

        return True

    @staticmethod
    def is_users_role(role: int) -> bool:
        return int(role) in USER_ROLES

    @staticmethod
    def is_type_address(type: int) -> bool:
        return int(type) in ADDRESS_TYPES

    @staticmethod
    def is_type_product(type: int) -> bool:
        return int(type) in PRODUCT_TYPES

    @staticmethod
    def is_type_subscription(type: int) -> bool:
        return int(type) in SUBSCRIPTION_TYPES

    @staticmethod
    def is_status_product(status: int) -> bool:
        return int(status) in PRODUCT_STATUS

    @staticmethod
    def is_status_order(status: int) -> bool:
        return int(status) in ORDER_STATUS

    @staticmethod
    def is_status_payment(status: int) -> bool:
        return int(status) in PAYMENT_STATUS

    @staticmethod
    def is_status_ticket(status: int) -> bool:
        return int(status) in TICKET_STATUS

    @staticmethod
    def is_valid_date(date) -> bool:
        try:
            datetime.fromtimestamp(date)
            return True
        except:
            return False

    @staticmethod
    def is_valid_image_format(file: UploadedFile) -> bool:
        _, ext = os.path.splitext(file.name.lower())
        return ext in ALLOWED_IMAGE_EXTENSIONS

    @staticmethod
    def is_valid_locale(locale: str) -> bool:
        if locale in ["en", "fr"]:
            return True
        else:
            return False

    @staticmethod
    def is_list_of_str_dicts(value) -> bool:
        if not isinstance(value, list):
            return False

        for item in value:
            if not isinstance(item, dict):
                return False
            for key, val in item.items():
                if not isinstance(key, str) or not isinstance(val, str):
                    return False

        return True

import re

# User Roles
USER_ROLES = [0, 1]

# Types
ADDRESS_TYPES = [0, 1]
PRODUCT_TYPES = [0, 1]
SUBSCRIPTION_TYPES = [0, 1]

# Status
PRODUCT_STATUS = [0, 1]
ORDER_STATUS = [0, 1, 2, 3, 4]
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
    def is_valid_id(id: int) -> bool:
        if id > 0:
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
    def is_type_address(type: int) -> bool:
        return int(type) in ADDRESS_TYPES

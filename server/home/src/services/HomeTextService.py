from home.src.data.repositories.HomeTextRepo import HomeTextRepo
from home.models import HomeText


class HomeTextService:

    @staticmethod
    def add(locale: str, text: str) -> HomeText | None:
        try:
            return HomeTextRepo.add(locale, text)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get(locale: str) -> HomeText | None:
        try:
            return HomeTextRepo.get(locale)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_all() -> list[HomeText] | None:
        try:
            return HomeTextRepo.get_all()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update(locale: str, text: str) -> HomeText | None:
        try:
            return HomeTextRepo.update(locale, text)
        except Exception as e:
            print(e)
            return None

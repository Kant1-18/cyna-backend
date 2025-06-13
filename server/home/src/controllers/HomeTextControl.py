from home.src.services.HomeTextService import HomeTextService
from home.src.data.models.HomeText import HomeText
from ninja.errors import HttpError
from utils.CheckInfos import CheckInfos
from users.src.services.AuthService import AuthService


class HomeTextControl:

    @staticmethod
    def add(request, data) -> HomeText | HttpError:
        if AuthService.is_admin(request):
            if not CheckInfos.is_valid_locale(data.locale):
                raise HttpError(400, "Invalid locale")
            if not CheckInfos.is_valid_string(data.text):
                raise HttpError(400, "Invalid text")
            home_text = HomeTextService.add(data.locale, data.text)
            if home_text:
                return home_text.to_json()
            else:
                raise HttpError(500, "Error when adding home text")
        else:
            raise HttpError(403, "Forbidden")

    @staticmethod
    def get(request, locale: str) -> HomeText | HttpError:
        if not CheckInfos.is_valid_locale(locale):
            raise HttpError(400, "Invalid locale")
        home_text = HomeTextService.get(locale)
        if home_text:
            return home_text.to_json()
        else:
            raise HttpError(404, "Home text not found")

    @staticmethod
    def get_all() -> list[HomeText]:
        home_texts = HomeTextService.get_all()
        if home_texts:
            return [home_text.to_json() for home_text in home_texts]
        else:
            raise HttpError(404, "No home texts found")

    @staticmethod
    def update(request, data) -> HomeText | HttpError:
        if AuthService.is_admin(request):
            if not CheckInfos.is_valid_locale(data.locale):
                raise HttpError(400, "Invalid locale")
            if not CheckInfos.is_valid_string(data.text):
                raise HttpError(400, "Invalid text")
            home_text = HomeTextService.update(data.locale, data.text)
            if home_text:
                return home_text.to_json()
            else:
                raise HttpError(500, "Error when updating home text")
        else:
            return HttpError(403, "Forbidden")

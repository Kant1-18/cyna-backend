from home.models import HomeText


class HomeTextRepo:

    @staticmethod
    def add(locale: str, text: str) -> HomeText:
        try:
            home_text = HomeText(locale=locale, text=text)
            home_text.save()
            return home_text
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get(locale: str) -> HomeText | None:
        try:
            home_text = HomeText.objects.get(locale=locale)
            return home_text
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_all() -> list[HomeText]:
        try:
            home_texts = HomeText.objects.all()
            return home_texts
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update(locale: str, text: str) -> HomeText:
        try:
            home_text = HomeText.objects.get(locale=locale)
            home_text.text = text
            home_text.save()
            return home_text
        except Exception as e:
            print(e)
            return None

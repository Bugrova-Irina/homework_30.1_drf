from rest_framework.serializers import ValidationError


class YoutubeURLValidator:
    """
    Проверка на присутствие в описании
    каких-либо других ссылок кроме youtube
    """

    def __call__(self, field_value):
        # Если поле пустое, пропускаем проверку
        if not field_value:
            return

        youtube_patterns = [
            "https://youtube.com",
            "https://www.youtube.com",
            "http://youtube.com",
            "http://www.youtube.com",
            "https://youtu.be",
        ]

        # Проверяем, начинается ли строка с https://youtube.com
        if not any(field_value.startswith(pattern) for pattern in youtube_patterns):
            raise ValidationError("Ссылка на видео должна быть с YouTube")

from rest_framework.validators import ValidationError


# def validate_url(value):
#     if 'youtube.com' not in value:
#         raise ValidationError("Ссылка может быть только со страницы youtube")


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value.get("link"):
            if "youtube.com" not in value.get("link"):
                raise ValidationError("Ссылка может быть только со страницы youtube")

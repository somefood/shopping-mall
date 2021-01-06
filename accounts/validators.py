from django.core.exceptions import ValidationError


def validate_isdigit(value: str) -> None:
    if not value.isdigit():
        msg = u"숫자만 입력해주세요."
        raise ValidationError(msg)
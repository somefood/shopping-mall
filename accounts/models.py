from django.db import models
from django.conf import settings
from .validators import validate_isdigit


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=50, verbose_name='닉네임')
    phone_number = models.CharField(max_length=11, verbose_name='전화번호', validators=[validate_isdigit])
    birth_day = models.CharField(max_length=8, verbose_name='생년월일', validators=[validate_isdigit])

    def __str__(self):
        return f"{self.user}-{self.nickname}"

    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = '프로필'


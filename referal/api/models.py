from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.BigIntegerField(
        verbose_name="Номер телефона",
        blank=False,
        unique=True,
        null=True,
    )
    refer_number = models.CharField(unique=True, max_length=6)
    otp = models.BigIntegerField(
        default=None,
        blank=False,
        null=True,
    )
    foreign_referal = models.CharField(max_length=6)

    def __int__(self):
        return self.phone_number

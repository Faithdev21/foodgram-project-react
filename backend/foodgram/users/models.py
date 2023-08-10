from django.contrib.auth.models import AbstractUser
from django.db import models

from api import constants
from users.validators import (validate_email_length,
                              validate_name_and_lastname, validate_password,
                              validate_username, validate_username_length)


class User(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField(
        verbose_name='email адрес',
        unique=True,
        null=False,
        max_length=constants.USER_EMAIL_MAX_LENGTH,
        validators=[validate_email_length]
    )
    username = models.CharField(
        verbose_name='username',
        max_length=constants.USER_NAME_MAX_LENGTH,
        null=False,
        unique=True,
        validators=[validate_username, validate_username_length]
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=constants.USER_NAME_MAX_LENGTH,
        null=False,
        validators=[validate_name_and_lastname]
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=constants.USER_NAME_MAX_LENGTH,
        null=False,
        validators=[validate_name_and_lastname]
    )
    password = models.CharField(
        verbose_name='пароль',
        max_length=constants.PASSWORD_MAX_LENGTH,
        null=False,
        validators=[validate_password]
    )
    is_subscribed = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

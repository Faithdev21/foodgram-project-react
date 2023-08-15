import getpass
import re

from rest_framework import status
from rest_framework.exceptions import ValidationError

from api import constants


def validate_username(value: str) -> str:
    """Валидация не является ли username =='me'."""
    if value.lower() == 'me':
        raise ValidationError(
            'me не валидный username!'
        )
    if not bool(re.match(r'^[\w.@+-]+$', value)):
        raise ValidationError(
            'username содержит некорректный символ'
        )
    return value


def validate_username_length(value: str) -> None:
    """Валидация длины поля username."""
    if len(value) > constants.USER_NAME_MAX_LENGTH:
        raise ValidationError('Длина не должна превышать 150 символов',
                              code=status.HTTP_400_BAD_REQUEST)


def validate_email_length(value: str) -> None:
    """Валидация длины поля email."""
    if len(value) > constants.USER_EMAIL_MAX_LENGTH:
        raise ValidationError('Длина не должна превышать 254 символа',
                              code=status.HTTP_400_BAD_REQUEST)


def validate_name_and_lastname(value: str) -> None:
    """Валидация на наличие только букв в имени и фамилии."""
    if not bool(re.match(r'^[A-zА-яЁё]+$', value)):
        raise ValidationError(
            'В имени и фамилии могут быть только буквы'
        )


def validate_password(value: str) -> None:
    """Валидация пароля."""
    pattern_password = (
        r'^(?=.*[a-z])'
        r'(?=.*[A-Z])'
        r'(?=.*\d)'
        r'(?=.*[@$!%*#?&])'
        r'[A-Za-z\d@$!#%*?&]{8,150}$'
    )
    user_input = getpass.getpass()
    if not re.search(pattern_password, user_input):
        raise ValidationError(
            'Пароль должен состоять как минимум из 8 символов,'
            'заглавной буквы, строчной буквы, цифры и символа'
            'для обеспечения безопасности'
        )


def validate_number(value) -> None:
    """Валидация минимального и максимального числа."""
    if constants.NUMBER_MAX < value < constants.NUMBER_MIN:
        raise ValidationError('Число не больше 32000 символов и не меньше 1',
                              code=status.HTTP_400_BAD_REQUEST)

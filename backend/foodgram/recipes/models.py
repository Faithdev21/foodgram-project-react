from typing import Tuple

from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель Тегов."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    color = models.CharField(max_length=7)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        db_index=True,
        null=False, blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Описание рецепта',
        help_text='Введите описание',
        null=False, blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингридиенты',
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Tag',
        blank=False
    )
    cooking_time = models.PositiveIntegerField(
        null=False, blank=False
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        null=False, blank=False
    )
    is_favorited = models.BooleanField(
        default=False,
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering: Tuple = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель, связывающая рецепты и ингредиенты."""
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()


class Subscribe(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_followers'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='follow_user_following_check'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.user

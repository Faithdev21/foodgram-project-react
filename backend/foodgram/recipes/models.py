from django.db import models

from users.models import User
from users.validators import validate_number


class Tag(models.Model):
    """Модель Тегов."""
    name = models.CharField(
        max_length=200, verbose_name='Название тега'
    )
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name='Слаг тега'
    )
    color = models.CharField(max_length=7, verbose_name='Цвет тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=200, verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        db_index=True,
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описание',
        null=False,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингридиент',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки рецепта',
        null=False,
        validators=[validate_number]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='recipes/images/',
        null=False,
    )
    is_favorited = models.BooleanField(
        verbose_name='В избранном ',
        default=False,
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='В списке товаров',
        default=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель, связывающая рецепты и ингредиенты."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[validate_number]
    )

    class Meta:
        verbose_name = 'Количество ингредиентов в рецепте'
        ordering = ('recipe__name',)

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


class Subscribe(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='follower',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        verbose_name='Пользователь на которого подписан пользователь',
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
        ordering = ('user__username',)

    def __str__(self):
        return self.user

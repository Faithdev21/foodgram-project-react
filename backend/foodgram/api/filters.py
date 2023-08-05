from typing import Tuple

import django_filters
from django_filters import CharFilter
from django_filters.rest_framework import BooleanFilter

from recipes.models import Ingredient, Recipe


class RecipeFilter(django_filters.FilterSet):
    """Фильтрация по избранному, автору и списку покупок."""
    is_favorited = BooleanFilter(field_name="is_favorited")
    is_in_shopping_cart = BooleanFilter(field_name="is_in_shopping_cart")
    author = CharFilter(field_name='author__username')

    class Meta:
        model = Recipe
        fields: Tuple[str, ...] = (
            'is_favorited',
            'author',
            'is_in_shopping_cart',
        )


class IngredientFilter(django_filters.FilterSet):
    """Фильтрация по имени ингредиента."""
    name = CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields: Tuple[str, ...] = ('name',)

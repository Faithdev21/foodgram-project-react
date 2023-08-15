from typing import Tuple

from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import BooleanFilter

from recipes.models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    """Фильтрация по избранному, автору и списку покупок."""
    is_favorited = BooleanFilter(field_name="is_favorited")
    is_in_shopping_cart = BooleanFilter(field_name="is_in_shopping_cart")
    author = CharFilter(field_name='author__id')

    class Meta:
        model = Recipe
        fields: Tuple[str, ...] = (
            'is_favorited',
            'author',
            'is_in_shopping_cart',
        )


class IngredientFilter(FilterSet):
    """Фильтрация по имени ингредиента."""
    name = CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields: Tuple[str, ...] = ('name',)

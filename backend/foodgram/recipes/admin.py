from typing import Tuple

from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient, Subscribe, Tag
from users.models import User


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines: Tuple = (RecipeIngredientInline,)
    list_filter: Tuple = ('pub_date', 'name', 'author', 'tags')
    list_display: Tuple = ('name', 'author', 'total_favorites')
    search_fields: Tuple = ('name', 'author', 'tags')
    ordering: Tuple = ('name',)

    def total_favorites(self, obj):
        return Recipe.objects.filter(is_favorited=True).count()

    total_favorites.short_description = 'В избранном'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display: Tuple = ('username', 'email',)
    search_fields: Tuple = ('username', 'email',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    pass

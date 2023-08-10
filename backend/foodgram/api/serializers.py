import base64
import uuid
from typing import Dict, Optional, Tuple

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.utils.serializer_helpers import ReturnDict

from recipes.models import Ingredient, Recipe, RecipeIngredient, Subscribe, Tag
from api import constants
from users.models import User


class Base64ImageField(serializers.ImageField):
    """Кодировка изображений в формате base64."""

    def to_internal_value(self, data) -> uuid.UUID:
        """Ввод является допустимой строкой UUID"""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CustomUserSerializer(UserSerializer):
    """Сериализатор для чтения модели User'а."""

    class Meta:
        model = User
        fields: tuple[str] = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            is_subscribed = request.user.follower.filter(
                following=instance
            ).exists()
            representation['is_subscribed'] = is_subscribed
        return representation


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания модели User'а."""

    class Meta:
        model = User
        fields: Tuple[str, ...] = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields: Tuple[str, ...] = ('id', 'name', 'color', 'slug')
        lookup_field = 'slug'


class IngredientReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра ингредиентов."""

    class Meta:
        model = Ingredient
        fields: Tuple[str, ...] = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для поля ingredients
    в сериализаторе RecipeReadSerializer."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields: Tuple[str, ...] = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецептов."""
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipe_ingredients'
    )
    author = CustomUserSerializer()

    class Meta:
        model = Recipe
        fields: Tuple[str, ...] = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')


class CustomIngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор поля ingredients в сериализаторе создания рецептов."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = IntegerField(
        max_value=constants.NUMBER_MAX, min_value=constants.NUMBER_MIN
    )

    class Meta:
        model = RecipeIngredient
        fields: Tuple[str, ...] = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов."""
    ingredients = CustomIngredientCreateSerializer(many=True)
    image = Base64ImageField(required=True)
    cooking_time = IntegerField(
        max_value=constants.NUMBER_MAX, min_value=constants.NUMBER_MIN
    )

    class Meta:
        model = Recipe
        fields: Tuple[str, ...] = (
            'ingredients',
            'tags',
            'name',
            'text',
            'image',
            'cooking_time'
        )

    def validate(self, data: Dict) -> Dict:
        """Валидация на наличие ингредиентов и тегов в рецепте."""
        ingredients = data.get('ingredients')
        tags = data.get('tags')

        if not ingredients:
            raise serializers.ValidationError("Ingredients field is required.")

        if not tags:
            raise serializers.ValidationError("Tags field is required.")

        return data

    def create(self, validated_data: Dict) -> ReturnDict:
        """Создает и возвращает объект рецепта."""
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)

        recipe_ingredients = [
            RecipeIngredient(
                recipe=instance,
                ingredient=ingredient_data.get('ingredient'),
                amount=ingredient_data.get('amount')
            )
            for ingredient_data in ingredients
        ]
        instance.recipe_ingredients.bulk_create(recipe_ingredients)
        return instance

    def update(self, instance: object, validated_data: Dict) -> object:
        """Обновляет и возвращает существующий объект рецепта."""
        ingredients_data = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)

        for ingredient_data in ingredients_data:
            ingredient = ingredient_data.get('ingredient')
            amount = ingredient_data.get('amount')
            instance.recipe_ingredients.update(
                amount=amount,
                ingredient=ingredient
            )
        return instance

    def to_representation(self, instance: object) -> object:
        """Возвращает представление объекта рецепта
        через RecipeReadSerializer сериалайзер."""
        return RecipeReadSerializer(instance).data


class CustomRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для Избранного и Списка покупок."""

    class Meta:
        model = Recipe
        fields: Tuple[str, ...] = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""
    email = serializers.EmailField(
        source='following.email',
        read_only=True
    )
    id = serializers.IntegerField(
        source='following.id',
        read_only=True
    )
    username = serializers.CharField(
        source='following.username',
        read_only=True
    )
    first_name = serializers.CharField(
        source='following.first_name',
        read_only=True
    )
    last_name = serializers.CharField(
        source='following.last_name',
        read_only=True
    )
    recipes = CustomRecipeSerializer(
        source='following.recipes',
        many=True,
        read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields: Tuple[str, ...] = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj: Subscribe) -> bool:
        """Возвращает True, если подписка существует."""
        if obj.user.is_authenticated:
            return obj.user.follower.filter(
                following=obj.following
            ).exists()

    def get_recipes_count(self, obj: Subscribe) -> Optional[int]:
        """Возвращает количество рецептов у пользователя
        на которого вы подписаны"""
        return obj.following.recipes.count()


class SubscribeCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания и удаления подписок."""

    class Meta:
        model = Subscribe
        fields = '__all__'

    def validate(self, data):
        following_user = data.get('following')
        user = data.get('user')
        if user == following_user:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя.'
            )
        if user.follower.filter(following=following_user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscribeSerializer(
            instance, context={'request': request}
        ).data

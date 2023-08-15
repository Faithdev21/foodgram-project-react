from typing import Optional, Tuple, Type

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api import constants
from api.actions import (download_shopping_cart, favorite, shopping_cart,
                         subscribe, subscriptions)
from api.filters import IngredientFilter, RecipeFilter
from api.mixins import CreateList, ListRetrieve
from api.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly, StaffAuthorOrReadOnly
from api.serializers import (CustomRecipeSerializer,
                             CustomUserCreateSerializer, CustomUserSerializer,
                             IngredientReadSerializer, RecipeCreateSerializer,
                             RecipeReadSerializer, SubscribeSerializer,
                             TagSerializer)
from recipes.models import Ingredient, Recipe, Subscribe, Tag


class CustomUserViewSet(UserViewSet):
    """Вьюсет пользователя."""
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'post']
    permission_classes = (StaffAuthorOrReadOnly,)

    def get_serializer_class(self) -> Type:
        """Возвращает сериализатор."""
        if self.action == "set_password":
            return SetPasswordSerializer
        if self.request.method == "POST":
            return CustomUserCreateSerializer
        return self.serializer_class

    @action(detail=False,
            methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def me(self, request: Request) -> Response:
        serializer = CustomUserSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(ListRetrieve):
    """Возвращает список тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_field = ('name',)
    pagination_class = CustomPagination


class IngredientViewSet(ListRetrieve):
    """Возвращает список ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientReadSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('name',)
    http_method_names = ('get',)
    pagination_class = CustomPagination


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    filter_backends: Tuple = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = RecipeFilter
    http_method_names: Tuple[str, ...] = ('get', 'post', 'patch', 'delete',)
    permission_classes: Tuple = (StaffAuthorOrReadOnly,)
    pagination_class = PageNumberPagination
    ordering_fields: Tuple[str, ...] = ('name',)

    def get_queryset(self) -> QuerySet:
        queryset = Recipe.objects.prefetch_related(
            'recipe_ingredients__ingredient', 'tags'
        ).all()
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags)
        return queryset.distinct()

    def get_serializer_class(self) -> Type:
        if self.action in constants.ACTION_METHODS:
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)

    def _update_and_response(
            self,
            request: Request,
            recipe: Recipe,
            field_name: str,
            error_message: str
    ) -> Response:
        if self.request.method == 'POST':
            field_value = getattr(recipe, field_name)
            if not field_value:
                setattr(recipe, field_name, True)
                recipe.save()
                serializer = CustomRecipeSerializer(
                    recipe,
                    context={'request': request}
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {'detail': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        if getattr(recipe, field_name):
            setattr(recipe, field_name, False)
            recipe.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': error_message},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=('POST', 'DELETE',),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk: Optional[int] = None) -> Response:
        return favorite(self, request, pk=pk)

    @action(
        detail=True,
        methods=('POST', 'DELETE',),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk: Optional[int] = None) -> Response:
        return shopping_cart(self, request, pk=pk)

    @action(
        detail=False,
        methods=('GET',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request: HttpRequest) -> HttpResponse:
        return download_shopping_cart(self, request)


class SubscribeViewSet(CreateList):
    """Возвращает все подписки пользователя."""
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> QuerySet:
        """Переопределение метода get_queryset
        для запроса фолловеров по username."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer) -> None:
        """Переопределение метода perform_create
        для сохранения фолловера при подписке на автора."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=('GET',))
    def subscriptions(self, request: Request) -> Response:
        return subscriptions(self, request)

    @action(detail=True, methods=('POST', 'DELETE',))
    def subscribe(
            self,
            request: Request,
            pk: Optional[int] = None
    ) -> Response:
        return subscribe(self, request, pk=pk)

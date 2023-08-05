from django.urls import include, path
from rest_framework import routers

from api.views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                       SubscribeViewSet, TagViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    'users/subscriptions', SubscribeViewSet, basename='subscriptions'
)
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('users/<int:pk>/subscribe/', SubscribeViewSet.as_view(
        {'post': 'subscribe', 'delete': 'subscribe'})),
    path('recipes/<int:pk>)/favorite/', RecipeViewSet.as_view(
        {'post': 'favorite', 'delete': 'favorite'})),
    path('recipes/<int:pk>)/shopping_cart/', RecipeViewSet.as_view(
        {'post': 'shopping_cart', 'delete': 'shopping_cart'})),
    path('api/recipes/download_shopping_cart/', RecipeViewSet.as_view(
        {'list': 'download_shopping_cart'})),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]

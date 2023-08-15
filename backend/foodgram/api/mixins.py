from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListRetrieve(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """Класс, включающий в себя list и retrieve методы."""


class CreateList(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    """Класс, включающий в себя create и list методы."""

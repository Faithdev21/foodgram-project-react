from typing import Any

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminOrReadOnly(BasePermission):
    """Полный доступ админ или только чтение."""

    def has_permission(self, request, view) -> bool:
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin
                )


class IsAdmin(BasePermission):
    """Доступ только админу."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (request.user.is_superuser
                or (request.user.is_authenticated and request.user.is_admin))


class StaffAuthorOrReadOnly(BasePermission):
    """Доступ админу или автору."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(
            self,
            request: Request,
            view: APIView,
            obj: Any
    ) -> bool:
        return (request.method in SAFE_METHODS
                or request.user.is_staff
                or obj.author == request.user)

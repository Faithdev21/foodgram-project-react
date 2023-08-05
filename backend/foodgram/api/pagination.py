from typing import Any

from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    """Кастомный пагинатор для вывода ответа без лишних полей."""
    def get_paginated_response(self, data: Any) -> Response:
        return Response(data)

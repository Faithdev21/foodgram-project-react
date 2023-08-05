from collections import defaultdict
from io import BytesIO
from typing import Dict, List, Optional

from django.http import HttpRequest, HttpResponse
from recipes.models import Ingredient, RecipeIngredient, Subscribe
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import User

from .serializers import SubscribeSerializer


def favorite(self, request: Request, pk: Optional[int] = None) -> Response:
    """Добавление рецепта в избранное или его удаление из избранного."""
    recipe = self.get_object()
    field_name: str = 'is_favorited'
    error_message: str = (
        'Рецепт уже находится в избранном!' if getattr(recipe, field_name)
        else 'Рецепт не находится в избранном!')
    return self._update_and_response(request, recipe,
                                     field_name, error_message)


def shopping_cart(
        self,
        request: Request,
        pk: Optional[int] = None
) -> Response:
    """Добавление рецепта в список покупок или его удаление оттуда."""
    recipe = self.get_object()
    field_name: str = 'is_in_shopping_cart'
    error_message: str = (
        'Рецепт уже находится в списке покупок!' if getattr(recipe, field_name)
        else 'Рецепт не находится в списке покупок!')
    return self._update_and_response(
        request, recipe, field_name, error_message
    )


def download_shopping_cart(self, request: HttpRequest) -> HttpResponse:
    """Скачивание списка покупок в PDF формате"""
    recipes_in_shopping_cart = RecipeIngredient.objects.filter(
        recipe__is_in_shopping_cart=True
    )

    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='RussianStyle', fontName='Arial', fontSize=12,
        alignment=TA_LEFT, spaceAfter=6, spaceBefore=6))

    ingredient_totals: Dict[str, int] = defaultdict(int)
    for recipe in recipes_in_shopping_cart:
        name = recipe.ingredient.name
        amount = recipe.amount
        ingredient_totals[name] += amount
    data: List[List[Paragraph]] = []

    unique_ingredient_names = list(ingredient_totals.keys())
    ingredients = Ingredient.objects.filter(name__in=unique_ingredient_names)
    ingredient_units = {
        ingredient.name: ingredient.measurement_unit
        for ingredient in ingredients
    }

    for name, total_amount in ingredient_totals.items():
        measurement_unit = ingredient_units[name]
        data.append(
            [Paragraph(
                f"• {name.strip()} - {total_amount}{measurement_unit.strip()}",
                styles['RussianStyle'])]
        )
    if not data:
        data.append(
            [Paragraph("СПИСОК ПОКУПОК ПУСТ.", styles['RussianStyle'])]
        )
    row_height = 30
    num_rows = len(data)
    rowHeights = [row_height] * num_rows

    table = Table(data, colWidths=500, rowHeights=rowHeights)
    style = TableStyle([
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial'),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.green),
    ])
    table.setStyle(style)
    doc = SimpleDocTemplate(buffer, pagesize=letter, bottomMargin=30)
    story: List[Paragraph | Spacer | Table] = []
    header_style = ParagraphStyle(
        name='HeaderStyle', fontName='Arial-Bold', fontSize=16,
        alignment=TA_CENTER, textColor=colors.black,
        spaceAfter=6, spaceBefore=6
    )
    header_text = "СПИСОК ПОКУПОК"
    header_paragraph = Paragraph(header_text, header_style)
    story.append(header_paragraph)
    story.append(Spacer(1, 20))
    story.append(table)
    footer_style = ParagraphStyle(
        name='FooterStyle', fontName='Arial', fontSize=14,
        alignment=TA_CENTER, textColor=colors.black, )
    footer_text = "<i>Приятного аппетита!</i>"
    footer_paragraph = Paragraph(footer_text, footer_style)
    story.append(Spacer(1, 20))
    story.append(footer_paragraph)
    doc.build(story)
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="shopping_list.pdf"'
    return response


def subscriptions(self, request: Request) -> Response:
    """Узнать на кого подписан пользователь"""
    subscriptions = self.get_queryset().select_related('following')
    serializer = SubscribeSerializer(
        subscriptions,
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)


def subscribe(self, request: Request, pk: Optional[int] = None) -> Response:
    """Добавление и удаление подписки на пользователя."""
    following_user = User.objects.get(pk=pk)
    if request.method == 'POST':
        if request.user == following_user:
            return Response(
                {'detail': 'Нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscribe.objects.filter(
                user=request.user,
                following=following_user
        ).exists():
            return Response(
                {'detail': 'Вы уже подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscribe, created = Subscribe.objects.get_or_create(
            user=request.user,
            following=following_user
        )
        subscribe.is_subscribe = True
        subscribe.save()
        serializer = SubscribeSerializer(
            subscribe,
            context={'request': request}
        )
        return Response(serializer.data)
    else:
        try:
            subscriptions = self.get_queryset().get(following=pk)
        except Subscribe.DoesNotExist:
            return Response(
                {'detail': 'Подписка не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
        subscriptions.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

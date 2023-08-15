import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных в таблицу Ингредиентов'

    def handle(self, *args, **kwargs):
        for row in csv.DictReader(
                open('data/ingredients.csv', encoding='utf-8')
        ):
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            ingredient.save()

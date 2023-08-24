# Foodgram project

### Foodram - это продуктовый помощник, сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

---

УСТАНОВКА ПРИЛОЖЕНИЯ:

1. Клонировать репозиторий и перейти в него в командной строке:
   git clone git@github.com:Faithdev21/foodgram-project-react
2. Cоздать и активировать виртуальное окружение:
   python3 -m venv venv
   source venv/bin/activate
3. Установить зависимости из файла requirements.txt:
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
4. Выполнить миграции:
   python3 manage.py migrate
5. Запустить проект:
   python3 manage.py runserver

---

ЗАГРУЗКА ТЕСТОВЫХ ДАННЫХ:

Тестовые данные ингредиентов
загружаются файлами в формате csv командой:

- `python manage.py import_csv`

---

ПРИМЕРЫ ЗАПРОСОВ

`/api/tags/`
GET -  Получение списка всех тегов.

`/api/tags/{id}`
GET - Получение тега по id.

`/api/ingredients/`

GET - Получение списка ингредиентов.

`/api/ingredients/{id}/`
GET - Получение ингредиента по id.

`/api/recipes/`

GET - Получение списка всех рецептов.
POST - Добавление рецепта.

`/api/recipes/{id}/`

GET - Получение информации о рецепте по id.
PATCH - Обновление рецепта.
DELETE - Удаление рецепта.

`/api/recipes/{id}/shopping_cart/`

DELETE - Удаление рецепта из списка покупок.
POST - Добавление рецепта в список покупок.

`/api/recipes/download_shopping_cart/`
GET - Cкачать список покупок (PDF)

`/api/recipes/{id}/favorite/`

POST - Добавление рецепта в избранное.
DELETE - Удаление рецепта из избранного.

`/api/users/`
GET - Получить список всех пользователей.

`/api/users/`
POST - Добавить нового пользователя.

`/api/users/me/`
GET - Получить данные своей учетной записи

`/api/users/{id}/`
GET - Получить пользователя по id.

`/api/users/subscriptions/`
GET -  Список подписок.

`/api/users/subscribe/`

POST - Подписаться на пользователя.
DELETE - Отписаться от пользователя.

`/api/users/set_password/`

POST - Изменить пароль.

`/api/auth/token/login/`

POST - Получить токен.
DELETE - Удалить токен.

---

АВТОР ПРОЕКТА:
🚀️ Егор Лоскутов https://github.com/Faithdev21

---

СТЕК ТЕХНОЛОГИЙ: При создании проекта были использованы следующие технологии:

> Python, Django, djangorestframework, Simple JWT, GIT, ReportLab

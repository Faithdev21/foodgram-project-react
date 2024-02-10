# Foodgram project

### Foodram - это продуктовый помощник, сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

---

УСТАНОВКА ПРИЛОЖЕНИЯ:

Клонировать репозиторий и перейти в него в командной строке:
   git clone git@github.com:Faithdev21/foodgram-project-react
   
Создайте файл /infra/.env
```
SECRET_KEY=django-insecure-r7=j=j2^+d-vx(rm%0wpa7b!r5t#wb#yeffoq2#co*^2(pg2oy
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,backend
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
Из директории с docker-compose.yaml выполните:

```docker-compose up -d```

Для пересборки образа (в случае обновления содержимого проекта) дополните команду так:

```docker-compose up -d --build```

Примените миграции:

```docker-compose exec backend python manage.py migrate```

Создайте суперюзера:

```docker-compose exec backend python manage.py createsuperuser```

Соберите статику:

```docker-compose exec backend python manage.py collectstatic --no-input```

---

ЗАГРУЗКА ТЕСТОВЫХ ДАННЫХ:

Тестовые данные ингредиентов
загружаются файлами в формате csv командой:

```docker-compose exec backend python manage.py import_csv```

**P.S. Добавьте хотя бы 1 тег через админку, чтобы корректно создавать рецепты**

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

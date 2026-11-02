<div align="center">

# 🧩 Sample DRF

**Готовый шаблон REST API на Django REST Framework: склонировал, переименовал — и пишешь бизнес-логику, а не настройки.**

[![CI](https://github.com/ArtaTOPprog/Sample_DRF/actions/workflows/ci.yml/badge.svg)](https://github.com/ArtaTOPprog/Sample_DRF/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-A30000)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64?logo=ruff&logoColor=black)

</div>

---

## ✨ Что внутри

| | Возможность | Чем сделано |
|---|---|---|
| 🔐 | Регистрация, вход, обновление и отзыв токенов, профиль, смена пароля | `djangorestframework-simplejwt` + blacklist |
| 👤 | Свой пользователь с уникальным email с первого дня | `AbstractUser` |
| 📝 | Пример ресурса «Заметки»: CRUD, только свои записи, закрепление | `ModelViewSet` + права `IsOwner` |
| 🔎 | Фильтры, поиск, сортировка, пагинация с `page_size` | `django-filter`, `SearchFilter`, `OrderingFilter` |
| 📚 | Swagger UI, ReDoc и OpenAPI-схема | `drf-spectacular` |
| ⚙️ | Настройки по окружениям: `local`, `test`, `production` | `python-decouple` + `.env` |
| 🐘 | PostgreSQL, если задан `POSTGRES_DB`, иначе SQLite | — |
| 🛡️ | HTTPS, HSTS, secure cookies, ограничение частоты запросов | настройки Django и DRF |
| 🩺 | Health-check с проверкой базы | `/api/health/` |
| 🧪 | 31 тест на pytest | `pytest-django` |
| 🐳 | Dockerfile (непривилегированный пользователь, gunicorn, whitenoise) и docker-compose | — |
| 🤖 | CI: линтер, тесты на PostgreSQL, проверка миграций и схемы, сборка образа | GitHub Actions |
| 🧹 | Линтер и форматтер, хуки перед коммитом | `ruff`, `pre-commit` |
| 🐞 | Debug Toolbar и Browsable API только в локальном окружении | `django-debug-toolbar` |

## 🚀 Быстрый старт

### Локально

Нужен Python 3.11 или новее.

```bash
git clone https://github.com/ArtaTOPprog/Sample_DRF.git
cd Sample_DRF

python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements/dev.txt

cp .env.example .env                 # Windows: copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Без `POSTGRES_DB` в `.env` проект работает на SQLite — ничего ставить не нужно.

### В Docker

```bash
cp .env.example .env
docker compose up --build
```

Поднимутся PostgreSQL и приложение на http://localhost:8000, миграции применятся сами.

## 🗺️ Адреса

| Адрес | Что там |
|---|---|
| http://localhost:8000/api/docs/ | Swagger UI — можно сразу пробовать запросы |
| http://localhost:8000/api/redoc/ | ReDoc |
| http://localhost:8000/api/schema/ | OpenAPI-схема (YAML) |
| http://localhost:8000/api/health/ | Health-check |
| http://localhost:8000/admin/ | Админка Django |
| http://localhost:8000/__debug__/ | Debug Toolbar (только `local`) |

## 📡 API

Все адреса ниже начинаются с `/api/v1/`. Кроме регистрации и получения токена, нужен заголовок `Authorization: Bearer <access>`.

### Авторизация — `auth/`

| Метод | Адрес | Что делает |
|---|---|---|
| `POST` | `auth/register/` | Регистрация, сразу возвращает пользователя и пару токенов |
| `POST` | `auth/token/` | Вход по `username` и `password` → `access` + `refresh` |
| `POST` | `auth/token/refresh/` | Новый `access` (и новый `refresh`, старый уходит в blacklist) |
| `POST` | `auth/token/verify/` | Проверить токен |
| `POST` | `auth/logout/` | Выход: `refresh` отправляется в blacklist |
| `GET` / `PATCH` | `auth/me/` | Профиль текущего пользователя |
| `POST` | `auth/change-password/` | Смена пароля |

### Заметки — `notes/`

| Метод | Адрес | Что делает |
|---|---|---|
| `GET` | `notes/` | Список своих заметок |
| `POST` | `notes/` | Создать заметку |
| `GET` / `PUT` / `PATCH` / `DELETE` | `notes/{id}/` | Работа с одной заметкой |
| `POST` | `notes/{id}/pin/` | Закрепить |
| `POST` | `notes/{id}/unpin/` | Открепить |

Параметры списка:

| Параметр | Пример | Описание |
|---|---|---|
| `search` | `?search=покупки` | Поиск по заголовку и тексту |
| `is_pinned`, `is_archived` | `?is_archived=false` | Фильтры |
| `created_after`, `created_before` | `?created_after=2026-01-01T00:00:00Z` | Период создания |
| `ordering` | `?ordering=-updated_at` | Сортировка: `created_at`, `updated_at`, `title` |
| `page`, `page_size` | `?page=2&page_size=50` | Пагинация, максимум 100 на страницу |

### Пример

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "ivan", "email": "ivan@example.com", "password": "S3cure-pass-123"}'

curl -X POST http://localhost:8000/api/v1/notes/ \
  -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить хлеб"}'
```

Ответ со списком:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "owner": "ivan",
      "title": "Купить хлеб",
      "content": "",
      "is_pinned": false,
      "is_archived": false,
      "created_at": "2026-11-02T23:04:23+03:00",
      "updated_at": "2026-11-02T23:04:23+03:00"
    }
  ]
}
```

Ошибки приходят в едином виде: `{"detail": "...", "code": "not_found"}`, ошибки валидации — словарём по полям.

## 📁 Структура

```text
Sample_DRF/
├── apps/
│   ├── core/              # общее: базовая модель с датами, пагинация, права, обработчик ошибок, health-check
│   ├── users/             # свой пользователь и авторизация на JWT
│   └── notes/             # пример ресурса — копируйте его для своих сущностей
├── config/
│   ├── settings/
│   │   ├── base.py        # общие настройки
│   │   ├── local.py       # разработка: DEBUG, Debug Toolbar, Browsable API, CORS для всех
│   │   ├── production.py  # прод: HTTPS, HSTS, whitenoise, проверка SECRET_KEY
│   │   └── test.py        # тесты: быстрый хешер паролей, без лимитов запросов
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tests/                 # pytest
├── requirements/
│   ├── base.txt           # зависимости для работы
│   └── dev.txt            # + тесты, линтер, Debug Toolbar
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml         # настройки pytest и ruff
├── .env.example
└── manage.py
```

## ⚙️ Переменные окружения

Все переменные — в [`.env.example`](.env.example). Главные:

| Переменная | По умолчанию | Описание |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.local` | Окружение: `local`, `production`, `test` |
| `DJANGO_SECRET_KEY` | небезопасный ключ | **Обязателен в production**, иначе приложение не запустится |
| `DJANGO_DEBUG` | `True` в `local` | В `production` всегда выключен |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Через запятую |
| `POSTGRES_DB` | пусто | Если задан — используется PostgreSQL, иначе SQLite |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` | `postgres`, —, `localhost`, `5432` | Подключение к PostgreSQL |
| `CORS_ALLOWED_ORIGINS` | пусто | Адреса фронтенда через запятую |
| `JWT_ACCESS_MINUTES`, `JWT_REFRESH_DAYS` | `30`, `7` | Время жизни токенов |
| `THROTTLE_ANON`, `THROTTLE_USER` | `100/hour`, `1000/hour` | Лимиты запросов |
| `LOG_LEVEL` | `INFO` | Уровень логов |

Сгенерировать секретный ключ:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🛠️ Команды

| Команда | Что делает |
|---|---|
| `make install` | Поставить зависимости и хуки pre-commit |
| `make run` | Запустить сервер разработки |
| `make migrations` / `make migrate` | Создать / применить миграции |
| `make superuser` | Создать администратора |
| `make test` | Запустить тесты |
| `make cov` | Тесты с отчётом о покрытии |
| `make lint` / `make format` | Проверить / отформатировать код |
| `make check` | Проверки Django, миграций и OpenAPI-схемы |
| `make docker-up` / `make docker-down` | Поднять / остановить Docker |

На Windows без `make` используйте команды из [`Makefile`](Makefile) напрямую, например `pytest` или `ruff check .`.

## 🧱 Как добавить свой ресурс

1. Создайте приложение: `mkdir apps/products && python manage.py startapp products apps/products`, в `apps.py` укажите `name = "apps.products"`.
2. Добавьте `"apps.products"` в `LOCAL_APPS` в `config/settings/base.py`.
3. Модель наследуйте от `apps.core.models.TimeStampedModel` — поля `created_at` и `updated_at` появятся сами.
4. Сериализатор, `ModelViewSet` и роутер сделайте по образцу `apps/notes/`. Для записей конкретного пользователя берите право `IsOwner` и фильтруйте `get_queryset` по `request.user`.
5. Подключите `urls.py` приложения в `api_v1` в `config/urls.py`.
6. `python manage.py makemigrations && python manage.py migrate`, добавьте тесты в `tests/`.

## 🚢 Деплой

```bash
docker build -t sample-drf .
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=... \
  -e DJANGO_ALLOWED_HOSTS=api.example.com \
  -e CSRF_TRUSTED_ORIGINS=https://api.example.com \
  -e POSTGRES_DB=... -e POSTGRES_USER=... -e POSTGRES_PASSWORD=... -e POSTGRES_HOST=... \
  sample-drf
```

Образ по умолчанию работает с `config.settings.production`: сам применяет миграции, запускает gunicorn (`GUNICORN_WORKERS`, по умолчанию 3), а статику раздаёт через whitenoise. Сервер ожидается за прокси с HTTPS, который передаёт `X-Forwarded-Proto`. Если HTTPS нет, задайте `DJANGO_SECURE_SSL_REDIRECT=False`.

## 📄 Лицензия

Шаблон свободно используйте как основу для своих проектов.

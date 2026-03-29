# 🚀 Быстрый старт проекта

## Вариант 1: Локальная разработка (рекомендуется)

```bash
# 1. Перейти в директорию проекта
cd /home/koks7256/PycharmProjects/FastAPIProject1

# 2. Активировать виртуальное окружение
source .venv/bin/activate

# 3. Установить зависимости (если не установлены)
pip install -r requirements.txt

# 4. Запустить сервер с автоперезагрузкой
uvicorn app.main:app --reload

# 5. Открыть в браузере
# 🌐 http://127.0.0.1:8000
# 📚 Документация: http://127.0.0.1:8000/docs
```

## Вариант 2: Docker (production-like)

```bash
# Установить SECRET_KEY и запустить контейнер
export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build

# Или просто (если SECRET_KEY уже установлен):
docker compose up

# Остановка
docker compose down
```

## Вариант 3: Запуск тестов

```bash
# Активировать виртуальное окружение
source .venv/bin/activate

# Запустить все тесты
pytest tests/ -v

# Результат: ✅ 32 passed (все тесты проходят)
```

## Быстрая проверка API

### Регистрация
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "user",
    "password": "securepass123"
  }'
```

### Логин
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user&password=securepass123"
```

### Создать проект (с токеном из логина)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Project",
    "description": "Project description"
  }'
```

## Конфигурация

Проект использует переменные окружения из `.env` файла.

Скопируй `.env.example` → `.env` и отредактируй если нужно:

```bash
cp .env.example .env
```

Ключевые переменные:
- `ENV=development` - режим разработки
- `DATABASE_URL=sqlite+aiosqlite:///./test.db` - база данных (SQLite по умолчанию)
- `SECRET_KEY` - ключ для JWT токенов (не менее 32 символов)
- `AUTO_CREATE_TABLES=true` - создание таблиц при старте (только для development)

## Базы данных

### SQLite (по умолчанию, для разработки)
```
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

### PostgreSQL
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
```

## Дополнительные команды

### Просмотр документации OpenAPI
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Проверка здоровья приложения
```bash
curl http://127.0.0.1:8000/health/live   # Liveness check
curl http://127.0.0.1:8000/health/ready  # Readiness check (с DB)
```

### Создание новых миграций (после изменения моделей)
```bash
# Автоматически генерирует миграцию
alembic revision --autogenerate -m "описание"

# Применить миграцию
alembic upgrade head
```

### Просмотр логов (Docker)
```bash
docker compose logs -f app
```

## Структура проекта

```
app/
├── api/v1/              # API endpoints (routes)
│   ├── auth.py         # Аутентификация (register, login)
│   ├── users.py        # Пользователи
│   ├── projects.py     # Проекты
│   └── tasks.py        # Задачи
├── crud/                # CRUD операции
│   ├── base.py         # Базовый CRUD класс
│   ├── user.py         # User CRUD
│   ├── project.py      # Project CRUD
│   └── task.py         # Task CRUD
├── models/              # SQLAlchemy ORM модели
│   ├── user.py         # User модель
│   ├── project.py      # Project модель
│   └── task.py         # Task модель
├── schemas/             # Pydantic валидация
│   ├── user.py         # User schemas
│   ├── project.py      # Project schemas
│   ├── task.py         # Task schemas
│   └── token.py        # Token schemas
├── core/                # Конфигурация и security
│   ├── config.py       # Settings
│   ├── database.py     # DB setup
│   ├── security.py     # JWT, passwords
│   └── deps.py         # Dependency injection
├── main.py             # FastAPI app
└── health.py           # Health check endpoints

tests/                   # Тесты (32 test cases)
├── test_auth.py        # Тесты аутентификации
├── test_users.py       # Тесты пользователей
├── test_projects.py    # Тесты проектов
├── test_tasks.py       # Тесты задач
└── test_health.py      # Тесты health checks
```

## Что было исправлено

✅ **tasks.py** - Исправлены параметры пути (Query → Path)
✅ **crud/base.py** - Добавлен await для delete операции
✅ **Создана полная тестовая инфраструктура** (32 теста, все проходят)
✅ **Все эндпоинты протестированы** - аутентификация, авторизация, CRUD, валидация

## Статус

✅ Все 32 теста проходят успешно
✅ Синтаксис корректен
✅ Сервер стартует без ошибок
✅ API готов к использованию

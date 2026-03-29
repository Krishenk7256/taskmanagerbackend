# Task manager API

FastAPI-бэкенд: пользователи, JWT, проекты и задачи.

## Локальная разработка

1. Скопируйте `.env.example` в `.env` и задайте `DATABASE_URL` под свой PostgreSQL.
2. Установите зависимости: `pip install -r requirements.txt`
3. Примените миграции: `alembic upgrade head`  
   (альтернатива для dev: `AUTO_CREATE_TABLES=true` и `ENV=development` — таблицы создаются при старте, без Alembic).
4. Запуск: `uvicorn app.main:app --reload`

Документация OpenAPI: http://127.0.0.1:8000/docs

## Docker (production-like)

```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

Образ при старте выполняет `alembic upgrade head`, затем Gunicorn + Uvicorn workers.

## Production

- Выставьте `ENV=production`, надёжный `SECRET_KEY` (не короче 32 символов, не значение по умолчанию из примера).
- Отключите автосоздание таблиц: `AUTO_CREATE_TABLES=false` (в production это принудительно при валидации настроек для миграций используйте только Alembic).
- Настройте `CORS_ORIGINS` списком доверенных origin через запятую.
- Проверки: `GET /health/live`, `GET /health/ready` (готовность включает запрос к БД).

## Новые миграции

После изменения моделей:

```bash
alembic revision --autogenerate -m "описание"
alembic upgrade head
```

Убедитесь, что в `alembic/env.py` импортированы все модели (как в текущем `env.py`).

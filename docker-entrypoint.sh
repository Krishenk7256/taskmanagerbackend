#!/bin/sh
set -e
cd /app
python -m alembic upgrade head
exec gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000 \
  -w "${WEB_CONCURRENCY:-2}" \
  --access-logfile - \
  --error-logfile -

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_CACHE_DIR=/tmp/poetry-cache \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    PORT=8000

WORKDIR /app/backend

RUN pip install --upgrade pip && \
    pip install poetry

COPY backend/pyproject.toml backend/poetry.lock* /app/backend/

RUN poetry install --only main --no-root

COPY backend/ /app/backend/

EXPOSE 8000

CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}"]

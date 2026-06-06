#!/bin/sh

set -e

DB_HOST="${POSTGRES_HOST:-}"
DB_PORT="${POSTGRES_PORT:-5432}"
PORT="${PORT:-8000}"

if [ -n "$DB_HOST" ]; then
  echo "Aguardando o PostgreSQL ($DB_HOST:$DB_PORT) iniciar..."
  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 0.5
  done
  echo "PostgreSQL pronto!"
fi

echo "Rodando migrations..."
python manage.py migrate --noinput

echo "Coletando arquivos estaticos..."
python manage.py collectstatic --noinput

if [ "${RUN_SEED_DEMO:-false}" = "true" ]; then
  echo "Rodando seed demo..."
  python manage.py seed_demo
fi

echo "Iniciando Gunicorn..."
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT}"

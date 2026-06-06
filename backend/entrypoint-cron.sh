#!/bin/sh

set -e

DB_HOST="${POSTGRES_HOST:-}"
DB_PORT="${POSTGRES_PORT:-5432}"

if [ -n "$DB_HOST" ]; then
  echo "Aguardando o PostgreSQL ($DB_HOST:$DB_PORT) iniciar..."
  while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 0.5
  done
  echo "PostgreSQL pronto!"
fi

printenv | sed 's/^\(.*\)$/export \1/g' > /app/backend/.cron_env

echo "Iniciando cron..."
exec cron -f

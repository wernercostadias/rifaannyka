set dotenv-load := true

backend_dir := "backend"
frontend_dir := "frontend"
poetry := "poetry"
poetry_cache_dir := ".poetry-cache"

default:
    just --list

setup:
    cd {{backend_dir}} && POETRY_CACHE_DIR={{poetry_cache_dir}} {{poetry}} install
    cd {{frontend_dir}} && npm install

makemigrations:
    cd {{backend_dir}} && POETRY_CACHE_DIR={{poetry_cache_dir}} {{poetry}} run python manage.py makemigrations rifa compras gateway notifications

migrate:
    cd {{backend_dir}} && POETRY_CACHE_DIR={{poetry_cache_dir}} {{poetry}} run python manage.py migrate

superuser:
    cd {{backend_dir}} && POETRY_CACHE_DIR={{poetry_cache_dir}} {{poetry}} run python manage.py createsuperuser

seed:
    cd {{backend_dir}} && POETRY_CACHE_DIR={{poetry_cache_dir}} {{poetry}} run python manage.py seed_demo

shell:
    cd {{backend_dir}} && POETRY_CACHE_DIR={{poetry_cache_dir}} {{poetry}} run python manage.py shell

django:
    cd {{backend_dir}} && POETRY_CACHE_DIR={{poetry_cache_dir}} {{poetry}} run python manage.py runserver 127.0.0.1:8000

frontend:
    cd {{frontend_dir}} && npm run dev

server:
    #!/usr/bin/env bash
    set -e
    trap 'kill 0' INT TERM EXIT
    just django &
    just frontend &
    wait

check:
    cd {{backend_dir}} && POETRY_CACHE_DIR={{poetry_cache_dir}} {{poetry}} run python manage.py check

test:
    cd {{backend_dir}} && POETRY_CACHE_DIR={{poetry_cache_dir}} {{poetry}} run python manage.py test apps.rifa apps.compras apps.gateway

clean-python:
    find . -type d -name __pycache__ -prune -exec rm -rf {} +

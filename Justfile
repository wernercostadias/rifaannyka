set dotenv-load := true

backend_dir := "backend"
frontend_dir := "frontend"
python := ".venv/bin/python"
pip := ".venv/bin/pip"

default:
    just --list

setup:
    python3 -m venv {{backend_dir}}/.venv
    cd {{backend_dir}} && {{pip}} install -r requirements.txt
    cd {{frontend_dir}} && npm install

makemigrations:
    cd {{backend_dir}} && {{python}} manage.py makemigrations rifa compras gateway notifications

migrate:
    cd {{backend_dir}} && {{python}} manage.py migrate

superuser:
    cd {{backend_dir}} && {{python}} manage.py createsuperuser

seed:
    cd {{backend_dir}} && {{python}} manage.py seed_demo

shell:
    cd {{backend_dir}} && {{python}} manage.py shell

django:
    cd {{backend_dir}} && {{python}} manage.py runserver 127.0.0.1:8000

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
    cd {{backend_dir}} && {{python}} manage.py check

test:
    cd {{backend_dir}} && {{python}} manage.py test apps.rifa apps.compras apps.gateway

clean-python:
    find . -type d -name __pycache__ -prune -exec rm -rf {} +

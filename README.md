# Rifa Beneficente

Aplicacao web para rifa beneficente com backend Django/DRF e frontend Nuxt/Vue.

## Backend

```bash
cd backend
export POETRY_CACHE_DIR=.poetry-cache
poetry install
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py seed_demo
poetry run python manage.py runserver
```

API local: `http://127.0.0.1:8000/api/v1/`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

App local: `http://localhost:3000/`

## Primeira Rifa

Para criar uma rifa demo com 200 numeros:

```bash
just seed
```

Ou manualmente:

1. Acesse o admin em `http://127.0.0.1:8000/admin/`.
2. Crie uma rifa com status `draft`.
3. Use o shell Django para gerar os numeros e ativar:

```bash
export POETRY_CACHE_DIR=.poetry-cache
poetry run python manage.py shell
```

```python
from apps.rifa.models import Raffle
from apps.rifa.services import activate_raffle

raffle = Raffle.objects.first()
activate_raffle(raffle)
```

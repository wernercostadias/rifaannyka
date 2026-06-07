# Rifa Beneficente

Aplicacao web para rifa beneficente com backend Django/DRF e frontend Nuxt/Vue.

## Ambientes

- Use [.env.example](/home/werner/rifa/.env.example:1) como base para desenvolvimento local.
- Use [.env.production.example](/home/werner/rifa/.env.production.example:1) como referencia das variaveis que precisam existir no EasyPanel.
- O backend escolhe os settings via `ENVIRONMENT`:
  - `local` -> `config.settings.local`
  - `production` -> `config.settings.production`
- Em producao, prefira configurar as variaveis no painel do EasyPanel em vez de versionar um `.env` real.

## Backend

```bash
cp .env.example .env
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

Se quiser usar Postgres localmente, defina `DATABASE_URL` no `.env`. Se nao definir, o projeto usa SQLite em `backend/db.sqlite3`.

## Frontend

```bash
cd frontend
npm install
npm run dev

Para desenvolvimento local do frontend, crie ou ajuste `frontend/.env`:

```env
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api/v1
NUXT_PUBLIC_MERCADOPAGO_PUBLIC_KEY=
NUXT_PUBLIC_ENABLE_PAYMENT_SIMULATION=true
```
```

App local: `http://localhost:3000/`

## Producao no EasyPanel

Defina estas variaveis no servico da API:

```env
ENVIRONMENT=production
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=seu-dominio-api
CORS_ALLOWED_ORIGINS=https://seu-dominio-frontend
DATABASE_URL=postgres://usuario:senha@host:5432/banco?sslmode=disable
NUXT_PUBLIC_API_BASE=https://seu-dominio-api/api/v1
NUXT_PUBLIC_MERCADOPAGO_PUBLIC_KEY=...
NUXT_PUBLIC_ENABLE_PAYMENT_SIMULATION=false
MERCADOPAGO_PUBLIC_KEY=...
MERCADOPAGO_ACCESS_TOKEN=...
MERCADOPAGO_WEBHOOK_SECRET=...
MERCADOPAGO_NOTIFICATION_URL=https://seu-dominio-api/api/v1/payments/webhook/mercadopago/
MERCADOPAGO_STATEMENT_DESCRIPTOR=RIFA ANNYKA
RUN_SEED_DEMO=false
```

No container de producao, o entrypoint roda `migrate` e `collectstatic` automaticamente.
Se quiser popular a rifa demo no deploy, defina `RUN_SEED_DEMO=true`. Como o comando
`seed_demo` atualiza a rifa demo existente, deixe essa variavel como `false` depois da
primeira carga se nao quiser sobrescrever os dados da rifa demo em todo deploy.

### Cron para reservas vencidas

Para liberar reservas vencidas automaticamente no EasyPanel, crie um segundo servico
no mesmo projeto usando o arquivo `Dockerfile.cron`.

- Nome sugerido: `annyka-cron`
- Dockerfile: `Dockerfile.cron`
- Mesmo conjunto de variaveis do backend/API
- Sem dominio publico

Esse servico executa `python manage.py expire_stale_purchases` a cada minuto e,
antes de expirar a reserva, tenta sincronizar pagamentos pendentes com o Mercado Pago.

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

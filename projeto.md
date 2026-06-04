# Projeto: Rifa Beneficente

## Visao Geral

Criar uma aplicacao web completa para uma rifa beneficente. Visitantes poderao visualizar uma rifa ativa, escolher numeros disponiveis, informar seus dados pessoais e gerar uma reserva/compra sem precisar criar conta.

O projeto tera:

- Backend em Django, Django REST Framework e SQLite no ambiente local.
- Banco PostgreSQL em producao.
- Admin do Django para gestao interna.
- Frontend em Nuxt/Vue com interface responsiva.
- Estrutura preparada para variaveis de ambiente.
- Arquitetura pronta para integrar Pix ou gateway externo.

## Objetivos

- Exibir uma rifa beneficente ativa com imagem, descricao, valor e data do sorteio.
- Permitir selecao de numeros disponiveis em uma grade.
- Reservar temporariamente os numeros selecionados.
- Vincular a compra ao primeiro nome, sobrenome, e-mail e celular do comprador.
- Evitar duplicidade de numeros reservados ou pagos.
- Liberar numeros quando a reserva expirar.
- Preparar fluxo de pagamento e webhook.
- Preparar logs de notificacoes futuras.

## Regras De Negocio

- O comprador nao cria conta e nao faz login.
- Cada compra deve ter comprador, rifa, numeros, valor total e status.
- Numeros selecionados devem ser reservados por um tempo definido.
- Numeros reservados ou pagos nao podem ser comprados por outra pessoa.
- Se a reserva vencer sem pagamento confirmado, os numeros voltam para disponivel.
- A confirmacao de pagamento muda a compra para paga e os numeros para pagos.
- Toda reserva de numeros deve usar transacao no banco para evitar disputa.
- O admin pode criar, editar, cancelar e finalizar rifas.

## Stack

### Backend

- Python
- Django
- Django REST Framework
- SQLite local
- PostgreSQL producao
- django-environ ou python-decouple para variaveis de ambiente
- Pillow para upload de imagem da rifa

### Frontend

- Nuxt
- Vue.js
- TypeScript quando possivel
- Componentes reutilizaveis
- Mobile first

## Estrutura Sugerida

```text
backend/
  manage.py
  config/
    settings/
      base.py
      local.py
      production.py
    urls.py
    wsgi.py
    asgi.py
  apps/
    core/
    rifa/
    compras/
    gateway/
    notifications/

frontend/
  components/
  composables/
  layouts/
  pages/
  assets/
  utils/
```

## Apps Django

### core

Responsavel por base compartilhada do backend.

Modelo abstrato `BaseModel`:

- `id`
- `created_at`
- `updated_at`
- `is_active`

Tambem deve conter utilitarios globais, helpers de data, configuracoes base e constantes compartilhadas quando fizer sentido.

### rifa

Responsavel pela rifa e pelos numeros.

Modelo `Raffle`:

- `title`
- `description`
- `beneficiary_name`
- `goal_description`
- `image`
- `price_per_number`
- `total_numbers`
- `start_date`
- `end_date`
- `draw_date`
- `status`: `draft`, `active`, `finished`, `canceled`
- `winner_number`
- `winner_name`

Modelo `RaffleNumber`:

- `raffle`
- `number`
- `status`: `available`, `reserved`, `paid`, `canceled`
- constraint unica para `raffle + number`

### compras

Responsavel por compradores, reservas e compras.

Modelo `Buyer`:

- `first_name`
- `last_name`
- `email`
- `phone`

Modelo `Purchase`:

- `raffle`
- `buyer`
- `total_amount`
- `status`: `pending`, `reserved`, `paid`, `expired`, `canceled`
- `reservation_expires_at`
- `payment_reference`

Modelo `PurchaseNumber`:

- `purchase`
- `raffle_number`

Servicos principais:

- Criar reserva.
- Calcular valor total.
- Bloquear numeros dentro de transacao.
- Expirar reserva.
- Confirmar pagamento.
- Cancelar compra.

### gateway

Responsavel por preparar pagamentos.

Modelo `Payment`:

- `purchase`
- `provider`
- `amount`
- `status`: `pending`, `paid`, `failed`, `canceled`, `refunded`
- `external_id`
- `qr_code`
- `qr_code_text`
- `paid_at`

Modelo `PaymentWebhookLog`:

- `provider`
- `payload`
- `received_at`
- `processed`

Servicos:

- `create_payment`
- `confirm_payment`
- `cancel_payment`
- `process_webhook`

### notifications

Responsavel por registrar e preparar notificacoes futuras.

Modelo `NotificationLog`:

- `buyer`
- `purchase`
- `channel`: `email`, `whatsapp`, `sms`
- `status`
- `payload`
- `sent_at`

Eventos futuros:

- Confirmacao de reserva.
- Confirmacao de pagamento.
- Aviso de vencimento da reserva.
- Aviso do sorteio.

## APIs Necessarias

### Rifas

- `GET /api/v1/raffles/active/`
- `GET /api/v1/raffles/{id}/`
- `GET /api/v1/raffles/{id}/numbers/`

### Compras

- `POST /api/v1/purchases/`
- `GET /api/v1/purchases/{reference}/`
- `POST /api/v1/purchases/{reference}/cancel-expired/`

### Pagamentos

- `POST /api/v1/payments/`
- `GET /api/v1/payments/{id}/`
- `POST /api/v1/payments/webhook/{provider}/`

## Fluxo Principal

1. Visitante acessa a pagina da rifa.
2. Frontend carrega rifa ativa e numeros.
3. Visitante escolhe numeros disponiveis.
4. Visitante informa primeiro nome, sobrenome, e-mail e celular.
5. Backend cria comprador, compra e reserva os numeros em transacao.
6. Sistema retorna referencia da compra e prazo de expiracao.
7. Visitante segue para pagamento.
8. Gateway gera dados do pagamento.
9. Pagamento confirmado muda compra e numeros para pagos.
10. Tela final mostra agradecimento e numeros comprados.

## Telas Frontend

### 1. Pagina Inicial Da Rifa

- Banner/imagem.
- Titulo.
- Descricao beneficente.
- Valor por numero.
- Data do sorteio.
- Progresso de numeros vendidos.
- Botao para escolher numeros.

### 2. Selecao De Numeros

- Grade de numeros.
- Status visual para disponivel, reservado, pago e selecionado.
- Resumo dos numeros escolhidos.
- Valor total.

### 3. Formulario Do Comprador

- Primeiro nome.
- Sobrenome.
- E-mail.
- Celular.
- Validacoes basicas.

### 4. Pagamento

- QR Code Pix quando existir.
- Codigo copia e cola.
- Status do pagamento.
- Botao para verificar pagamento.

### 5. Confirmacao

- Nome do comprador.
- Numeros comprados.
- Status da compra.
- Mensagem de agradecimento.

## Admin Django

O admin deve permitir:

- Gerenciar rifas.
- Gerenciar numeros.
- Ver compradores.
- Ver compras.
- Alterar status de compra quando necessario.
- Ver pagamentos.
- Ver logs de webhook.
- Ver logs de notificacao.

## Testes Basicos

- Criacao de rifa.
- Geracao/listagem de numeros.
- Reserva de numero.
- Bloqueio de numero duplicado.
- Expiracao de reserva.
- Confirmacao de pagamento.
- Consulta de compra por referencia.

## Fases De Implementacao

### Fase 1: Base Do Projeto

- Criar projeto Django.
- Configurar settings local/producao.
- Criar apps.
- Criar `BaseModel`.
- Configurar DRF.
- Ativar admin.

### Fase 2: Rifa E Numeros

- Criar modelos `Raffle` e `RaffleNumber`.
- Criar serializers.
- Criar endpoints de listagem e detalhe.
- Criar admin.
- Criar geracao inicial de numeros.

### Fase 3: Compras E Reservas

- Criar modelos de comprador, compra e numeros da compra.
- Criar service de reserva com transacao.
- Criar endpoint de compra.
- Criar expiracao de reserva.
- Criar testes de concorrencia basicos.

### Fase 4: Pagamento

- Criar modelos de pagamento.
- Criar service abstrato de pagamento.
- Criar provider fake/local para desenvolvimento.
- Criar endpoints de pagamento e webhook.

### Fase 5: Frontend

- Criar Nuxt.
- Criar tema visual.
- Criar componentes base.
- Criar paginas do fluxo.
- Integrar com API.

### Fase 6: Acabamento

- Melhorar validacoes.
- Ajustar responsividade.
- Revisar estados vazios/erro/carregamento.
- Criar seed de rifa de exemplo.
- Preparar deploy.

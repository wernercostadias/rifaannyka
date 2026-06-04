import json
import hmac
import hashlib
import uuid
from urllib import error, request

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.compras.models import Purchase
from apps.compras.services import confirm_purchase_payment

from .models import Payment, PaymentWebhookLog


MERCADOPAGO_API_BASE = "https://api.mercadopago.com"


def _mercadopago_request(*, method: str, path: str, payload: dict | None = None) -> dict:
    if not settings.MERCADOPAGO_ACCESS_TOKEN:
        raise ValidationError("MERCADOPAGO_ACCESS_TOKEN nao configurado.")

    body = None
    headers = {
        "Authorization": f"Bearer {settings.MERCADOPAGO_ACCESS_TOKEN}",
        "accept": "application/json",
    }

    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
        headers["X-Idempotency-Key"] = str(uuid.uuid4())

    req = request.Request(f"{MERCADOPAGO_API_BASE}{path}", data=body, headers=headers, method=method)

    try:
        with request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore")
        raise ValidationError(f"Erro ao comunicar com Mercado Pago: {details or exc.reason}") from exc
    except error.URLError as exc:
        raise ValidationError(f"Erro de rede ao comunicar com Mercado Pago: {exc.reason}") from exc


def _parse_signature_header(signature_header: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for part in signature_header.split(","):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def validate_mercadopago_signature(*, payload: dict, headers: dict, query_params: dict | None = None) -> tuple[bool, dict]:
    secret = settings.MERCADOPAGO_WEBHOOK_SECRET
    signature_header = headers.get("x-signature", "")
    request_id = headers.get("x-request-id", "")
    query_params = query_params or {}

    metadata = {
        "has_secret": bool(secret),
        "has_signature_header": bool(signature_header),
        "has_request_id": bool(request_id),
    }

    if not secret or not signature_header or not request_id:
        return False, metadata

    signature_data = _parse_signature_header(signature_header)
    ts = signature_data.get("ts", "")
    v1 = signature_data.get("v1", "")
    data_id = str(
        (payload.get("data") or {}).get("id")
        or query_params.get("data.id")
        or payload.get("id")
        or ""
    )

    metadata.update({
        "ts": ts,
        "v1_present": bool(v1),
        "data_id": data_id,
    })

    if not ts or not v1 or not data_id:
        return False, metadata

    manifest = f"id:{data_id};request-id:{request_id};ts:{ts};"
    expected = hmac.new(secret.encode("utf-8"), manifest.encode("utf-8"), hashlib.sha256).hexdigest()
    metadata["manifest"] = manifest

    return hmac.compare_digest(expected, v1), metadata


def _create_local_pix_payment(*, purchase: Purchase, provider: str) -> Payment:
    return Payment.objects.create(
        purchase=purchase,
        provider=provider,
        amount=purchase.total_amount,
        external_id=str(uuid.uuid4()),
        qr_code_text=f"PIX-LOCAL-{purchase.reference}",
        qr_code="",
    )


def _create_mercadopago_pix_payment(*, purchase: Purchase) -> Payment:
    notification_url = settings.MERCADOPAGO_NOTIFICATION_URL or None
    payload = {
        "type": "online",
        "total_amount": f"{purchase.total_amount:.2f}",
        "external_reference": str(purchase.reference),
        "processing_mode": "automatic",
        "transactions": {
            "payments": [
                {
                    "amount": f"{purchase.total_amount:.2f}",
                    "payment_method": {
                        "id": "pix",
                        "type": "bank_transfer",
                    },
                    "expiration_time": "PT24H",
                }
            ]
        },
        "payer": {
            "first_name": purchase.buyer.first_name,
            "last_name": purchase.buyer.last_name,
            "email": purchase.buyer.email,
            "identification": {
                "type": "CPF",
                "number": purchase.buyer.cpf,
            },
        },
    }

    if notification_url:
        payload["notification_url"] = notification_url

    response = _mercadopago_request(method="POST", path="/v1/orders", payload=payload)
    payment_data = ((response.get("transactions") or {}).get("payments") or [{}])[0]
    payment_method = payment_data.get("payment_method") or {}

    return Payment.objects.create(
        purchase=purchase,
        provider="mercadopago",
        amount=purchase.total_amount,
        external_id=str(response.get("id", "")),
        qr_code=payment_method.get("qr_code_base64", ""),
        qr_code_text=payment_method.get("qr_code", ""),
        status=Payment.Status.PENDING,
    )


def create_payment(*, purchase: Purchase, provider: str = "local_pix") -> Payment:
    if purchase.status != Purchase.Status.RESERVED:
        raise ValidationError("A compra precisa estar reservada para gerar pagamento.")

    if provider == "mercadopago":
        return _create_mercadopago_pix_payment(purchase=purchase)

    return _create_local_pix_payment(purchase=purchase, provider=provider)


def confirm_payment(payment: Payment) -> Payment:
    with transaction.atomic():
        payment = Payment.objects.select_for_update().get(id=payment.id)
        if payment.status == Payment.Status.PAID:
            return payment
        payment.status = Payment.Status.PAID
        payment.paid_at = timezone.now()
        payment.save(update_fields=["status", "paid_at", "updated_at"])
        confirm_purchase_payment(payment.purchase, payment_reference=str(payment.id))
    return payment


def cancel_payment(payment: Payment) -> Payment:
    payment.status = Payment.Status.CANCELED
    payment.save(update_fields=["status", "updated_at"])
    return payment


def _sync_mercadopago_payment(resource_id: str) -> bool:
    payment_details = _mercadopago_request(method="GET", path=f"/v1/payments/{resource_id}")
    external_reference = payment_details.get("external_reference")
    if not external_reference:
        return False

    payment = (
        Payment.objects.select_related("purchase")
        .filter(purchase__reference=external_reference, provider="mercadopago")
        .order_by("-created_at")
        .first()
    )
    if payment is None:
        return False

    status = payment_details.get("status")
    if status == "approved":
        confirm_purchase_payment(payment.purchase, payment_reference=str(resource_id))
        payment.status = Payment.Status.PAID
        payment.paid_at = timezone.now()
        payment.save(update_fields=["status", "paid_at", "updated_at"])
        return True

    if status in {"cancelled", "rejected"}:
        payment.status = Payment.Status.CANCELED
        payment.save(update_fields=["status", "updated_at"])
        return True

    return False


def process_webhook(*, provider: str, payload: dict, headers: dict | None = None, query_params: dict | None = None) -> PaymentWebhookLog:
    headers = headers or {}
    query_params = query_params or {}
    log_payload = {
        "payload": payload,
        "headers": headers,
        "query_params": query_params,
    }

    if provider == "mercadopago":
        is_valid, metadata = validate_mercadopago_signature(
            payload=payload,
            headers=headers,
            query_params=query_params,
        )
        log_payload["signature"] = metadata
        log = PaymentWebhookLog.objects.create(provider=provider, payload=log_payload)
        if not is_valid:
            return log

        resource_id = str((payload.get("data") or {}).get("id") or payload.get("id") or "")
        if resource_id:
            log.processed = _sync_mercadopago_payment(resource_id)
            log.save(update_fields=["processed", "updated_at"])
        return log

    log = PaymentWebhookLog.objects.create(provider=provider, payload=log_payload)

    payment_id = payload.get("payment_id")
    if payment_id:
        payment = Payment.objects.filter(id=payment_id).first()
        if payment and payload.get("status") == Payment.Status.PAID:
            confirm_payment(payment)
            log.processed = True
            log.save(update_fields=["processed", "updated_at"])
    return log

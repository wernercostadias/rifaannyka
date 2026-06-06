from datetime import timedelta
import hashlib
import hmac
from unittest.mock import patch

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.compras.models import Buyer, Purchase, PurchaseNumber
from apps.compras.services import create_purchase
from apps.gateway.models import Payment
from apps.gateway.services import create_payment
from apps.rifa.models import Raffle, RaffleNumber
from apps.rifa.services import activate_raffle


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def active_raffle():
    raffle = Raffle.objects.create(
        title="Rifa da Maria",
        description="Campanha beneficente",
        beneficiary_name="Maria",
        goal_amount=2500,
        price_per_number=5,
        total_numbers=10,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=10),
        draw_date=timezone.now() + timedelta(days=11),
    )
    activate_raffle(raffle)
    return raffle


@pytest.fixture
def reserved_purchase(active_raffle):
    return create_purchase(
        raffle_id=active_raffle.id,
        buyer_data={
            "first_name": "Ana",
            "last_name": "Silva",
            "email": "ana@example.com",
            "phone": "(91) 99999-1234",
            "cpf": "12345678909",
        },
        numbers=[1, 2],
    )


@pytest.mark.django_db
def test_raffles_active_returns_404_without_active_raffle(api_client):
    response = api_client.get("/api/v1/raffles/active/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_raffles_active_returns_active_raffle_details(api_client, active_raffle):
    response = api_client.get("/api/v1/raffles/active/")

    assert response.status_code == 200
    assert response.data["id"] == active_raffle.id
    assert response.data["status"] == Raffle.Status.ACTIVE
    assert response.data["goal_description"] == active_raffle.goal_description


@pytest.mark.django_db
def test_raffle_numbers_endpoint_returns_paid_owner_name(api_client, active_raffle):
    raffle_number = RaffleNumber.objects.create(
        raffle=active_raffle,
        number=999,
        status=RaffleNumber.Status.PAID,
    )
    buyer = Buyer.objects.create(
        first_name="Annyka",
        last_name="Yasmin",
        email="annyka@example.com",
        phone="91999999999",
        cpf="00000000000",
    )
    purchase = Purchase.objects.create(
        raffle=active_raffle,
        buyer=buyer,
        total_amount=5,
        status=Purchase.Status.PAID,
        reservation_expires_at=timezone.now(),
    )
    PurchaseNumber.objects.create(purchase=purchase, raffle_number=raffle_number)

    response = api_client.get(f"/api/v1/raffles/{active_raffle.id}/numbers/")

    assert response.status_code == 200
    paid_number = next(item for item in response.data if item["number"] == 999)
    assert paid_number["owner_name"] == "Annyka"


@pytest.mark.django_db
def test_create_purchase_endpoint_creates_reserved_purchase(api_client, active_raffle):
    response = api_client.post(
        "/api/v1/purchases/",
        {
            "raffle_id": active_raffle.id,
            "buyer": {
                "full_name": "Bruno Souza",
                "phone": "91988887777",
                "cpf": "98765432100",
            },
            "numbers": [3, 4],
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["status"] == Purchase.Status.RESERVED
    assert response.data["numbers"] == [3, 4]


@pytest.mark.django_db
def test_create_purchase_endpoint_can_create_payment_together(api_client, active_raffle):
    with patch("apps.gateway.services._mercadopago_request") as mercadopago_request:
        mercadopago_request.return_value = {
            "id": "ORD123",
            "transactions": {
                "payments": [
                    {
                        "payment_method": {
                            "qr_code_base64": "base64-qr",
                            "qr_code": "pix-code",
                        }
                    }
                ]
            },
        }
        response = api_client.post(
            "/api/v1/purchases/",
            {
                "raffle_id": active_raffle.id,
                "buyer": {
                    "full_name": "Bruno Souza",
                    "phone": "91988887777",
                    "cpf": "98765432100",
                },
                "numbers": [3, 4],
                "payment_provider": "mercadopago",
            },
            format="json",
        )

    assert response.status_code == 201
    assert response.data["purchase"]["status"] == Purchase.Status.RESERVED
    assert response.data["payment"]["status"] == Payment.Status.PENDING
    assert response.data["payment"]["qr_code_text"] == "pix-code"


@pytest.mark.django_db
def test_create_purchase_endpoint_releases_numbers_if_payment_fails(api_client, active_raffle):
    with patch("apps.gateway.services._mercadopago_request", side_effect=Exception("boom")):
        response = api_client.post(
            "/api/v1/purchases/",
            {
                "raffle_id": active_raffle.id,
                "buyer": {
                    "full_name": "Bruno Souza",
                    "phone": "91988887777",
                    "cpf": "98765432100",
                },
                "numbers": [3, 4],
                "payment_provider": "mercadopago",
            },
            format="json",
        )

    assert response.status_code == 400
    assert response.data["payment"] == "Nao foi possivel iniciar o pagamento agora."
    purchase = Purchase.objects.get(buyer__cpf="98765432100")
    assert purchase.status == Purchase.Status.CANCELED
    statuses = list(
        RaffleNumber.objects.filter(raffle=active_raffle, number__in=[3, 4]).values_list("status", flat=True)
    )
    assert statuses == [RaffleNumber.Status.AVAILABLE, RaffleNumber.Status.AVAILABLE]


@pytest.mark.django_db
def test_create_purchase_expires_stale_reservation_before_reusing_numbers(api_client, active_raffle):
    stale_purchase = create_purchase(
        raffle_id=active_raffle.id,
        buyer_data={
            "first_name": "Ana",
            "last_name": "Silva",
            "email": "ana@example.com",
            "phone": "91999999999",
            "cpf": "12345678909",
        },
        numbers=[5, 6],
    )
    stale_purchase.reservation_expires_at = timezone.now() - timedelta(minutes=1)
    stale_purchase.save(update_fields=["reservation_expires_at"])

    response = api_client.post(
        "/api/v1/purchases/",
        {
            "raffle_id": active_raffle.id,
            "buyer": {
                "full_name": "Bruno Souza",
                "phone": "91988887777",
                "cpf": "98765432100",
            },
            "numbers": [5, 6],
        },
        format="json",
    )

    stale_purchase.refresh_from_db()
    assert stale_purchase.status == Purchase.Status.EXPIRED
    assert response.status_code == 201
    assert response.data["status"] == Purchase.Status.RESERVED


@pytest.mark.django_db
def test_retrieve_purchase_endpoint_returns_purchase(api_client, reserved_purchase):
    response = api_client.get(f"/api/v1/purchases/{reserved_purchase.reference}/")

    assert response.status_code == 200
    assert response.data["reference"] == str(reserved_purchase.reference)
    assert response.data["numbers"] == [1, 2]


@pytest.mark.django_db
def test_latest_purchases_endpoint_returns_public_payload(api_client, reserved_purchase):
    response = api_client.get(f"/api/v1/purchases/latest/?raffle_id={reserved_purchase.raffle_id}")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["buyer_name"] == "Ana S."
    assert response.data[0]["buyer_phone"] == "91*****34"


@pytest.mark.django_db
def test_purchase_lookup_endpoint_finds_purchase_by_name(api_client, reserved_purchase):
    response = api_client.get(f"/api/v1/purchases/lookup/?raffle_id={reserved_purchase.raffle_id}&search=Ana Silva")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["buyer_name"] == "Ana Silva"
    assert response.data[0]["numbers"] == [1, 2]


@pytest.mark.django_db
def test_create_payment_endpoint_creates_pending_payment(api_client, reserved_purchase):
    response = api_client.post(
        "/api/v1/payments/",
        {
            "purchase_reference": str(reserved_purchase.reference),
            "provider": "local_pix",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["status"] == Payment.Status.PENDING
    assert response.data["provider"] == "local_pix"


@pytest.mark.django_db
def test_retrieve_payment_endpoint_returns_payment(api_client, reserved_purchase):
    payment = create_payment(purchase=reserved_purchase)

    response = api_client.get(f"/api/v1/payments/{payment.id}/")

    assert response.status_code == 200
    assert response.data["id"] == payment.id
    assert response.data["status"] == Payment.Status.PENDING


@pytest.mark.django_db
def test_payment_status_endpoint_returns_payment_and_purchase(api_client, reserved_purchase):
    payment = create_payment(purchase=reserved_purchase)

    response = api_client.get(f"/api/v1/payments/{payment.id}/status/")

    assert response.status_code == 200
    assert response.data["payment"]["id"] == payment.id
    assert response.data["purchase"]["reference"] == str(reserved_purchase.reference)


@pytest.mark.django_db
def test_payment_status_endpoint_expires_purchase_when_reservation_is_stale(api_client, reserved_purchase):
    payment = create_payment(purchase=reserved_purchase)
    reserved_purchase.reservation_expires_at = timezone.now() - timedelta(minutes=1)
    reserved_purchase.save(update_fields=["reservation_expires_at"])

    response = api_client.get(f"/api/v1/payments/{payment.id}/status/")

    assert response.status_code == 200
    assert response.data["purchase"]["status"] == Purchase.Status.EXPIRED


@pytest.mark.django_db
def test_confirm_local_payment_endpoint_marks_payment_as_paid(api_client, reserved_purchase):
    payment = create_payment(purchase=reserved_purchase)

    response = api_client.post(f"/api/v1/payments/{payment.id}/confirm-local/")

    assert response.status_code == 200
    assert response.data["status"] == Payment.Status.PAID
    reserved_purchase.refresh_from_db()
    assert reserved_purchase.status == Purchase.Status.PAID


@pytest.mark.django_db
def test_local_webhook_endpoint_confirms_payment(api_client, reserved_purchase):
    payment = create_payment(purchase=reserved_purchase)

    response = api_client.post(
        "/api/v1/payments/webhook/local_pix/",
        {
            "payment_id": payment.id,
            "status": Payment.Status.PAID,
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["processed"] is True
    payment.refresh_from_db()
    assert payment.status == Payment.Status.PAID


@pytest.mark.django_db
def test_mercadopago_webhook_endpoint_processes_signed_payload(api_client, reserved_purchase, settings):
    payment = Payment.objects.create(
        purchase=reserved_purchase,
        provider="mercadopago",
        amount=reserved_purchase.total_amount,
        external_id="ORD123",
        status=Payment.Status.PENDING,
    )
    secret = "test-secret"
    request_id = "req-abc"
    ts = "1710000000"
    manifest = "id:ORD123;request-id:req-abc;ts:1710000000;"
    signature = hmac.new(secret.encode("utf-8"), manifest.encode("utf-8"), hashlib.sha256).hexdigest()

    with patch("apps.gateway.services._mercadopago_request") as mercadopago_request:
        mercadopago_request.return_value = {
            "id": "ORD123",
            "external_reference": str(reserved_purchase.reference),
            "status": "processed",
            "status_detail": "accredited",
            "transactions": {
                "payments": [
                    {
                        "id": "PAY123",
                        "status": "processed",
                        "status_detail": "accredited",
                    }
                ]
            },
        }
        settings.MERCADOPAGO_WEBHOOK_SECRET = secret
        response = api_client.post(
            "/api/v1/payments/webhook/mercadopago/?data.id=ORD123&type=order",
            {"data": {"id": "ORD123"}},
            format="json",
            HTTP_X_SIGNATURE=f"ts={ts},v1={signature}",
            HTTP_X_REQUEST_ID=request_id,
        )

    assert response.status_code == 200
    assert response.data["processed"] is True
    payment.refresh_from_db()
    reserved_purchase.refresh_from_db()
    assert payment.status == Payment.Status.PAID
    assert reserved_purchase.status == Purchase.Status.PAID

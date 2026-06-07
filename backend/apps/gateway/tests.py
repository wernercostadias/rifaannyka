from datetime import timedelta
import hashlib
import hmac
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.compras.models import Purchase
from apps.compras.services import create_purchase
from apps.rifa.models import Raffle, RaffleNumber
from apps.rifa.services import activate_raffle

from .models import Payment
from .services import confirm_payment, create_payment, process_webhook, validate_mercadopago_signature


class PaymentServiceTests(TestCase):
    def setUp(self):
        self.raffle = Raffle.objects.create(
            title="Rifa da Maria",
            description="Campanha beneficente",
            beneficiary_name="Maria",
            price_per_number=10,
            total_numbers=10,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=10),
            draw_date=timezone.now() + timedelta(days=11),
        )
        activate_raffle(self.raffle)
        self.purchase = create_purchase(
            raffle_id=self.raffle.id,
            buyer_data={
                "first_name": "Ana",
                "last_name": "Silva",
                "email": "ana@example.com",
                "phone": "91999999999",
                "cpf": "12345678909",
            },
            numbers=[7, 8],
        )

    def test_create_payment_for_reserved_purchase(self):
        payment = create_payment(purchase=self.purchase)

        self.assertEqual(payment.status, Payment.Status.PENDING)
        self.assertEqual(payment.amount, self.purchase.total_amount)
        self.assertIn(str(self.purchase.reference), payment.qr_code_text)

    def test_confirm_payment_marks_purchase_and_numbers_as_paid(self):
        payment = create_payment(purchase=self.purchase)

        confirm_payment(payment)

        payment.refresh_from_db()
        self.purchase.refresh_from_db()
        self.assertEqual(payment.status, Payment.Status.PAID)
        self.assertEqual(self.purchase.status, Purchase.Status.PAID)
        self.assertEqual(
            RaffleNumber.objects.filter(number__in=[7, 8], status=RaffleNumber.Status.PAID).count(),
            2,
        )

    @patch("apps.gateway.services.time.sleep", return_value=None)
    @patch("apps.gateway.services._mercadopago_request")
    def test_create_mercadopago_payment_fetches_order_when_post_response_has_no_qr(
        self,
        mercadopago_request,
        _sleep,
    ):
        mercadopago_request.side_effect = [
            {
                "id": "ORD123",
                "transactions": {
                    "payments": [
                        {
                            "id": "PAY123",
                            "payment_method": {
                                "qr_code": "",
                                "qr_code_base64": "",
                            },
                        }
                    ]
                },
            },
            {
                "id": "ORD123",
                "transactions": {
                    "payments": [
                        {
                            "id": "PAY123",
                            "payment_method": {
                                "qr_code": "pix-code",
                                "qr_code_base64": "base64-qr",
                            },
                        }
                    ]
                },
            },
        ]

        payment = create_payment(purchase=self.purchase, provider="mercadopago")

        self.assertEqual(payment.external_id, "ORD123")
        self.assertEqual(payment.qr_code_text, "pix-code")
        self.assertEqual(payment.qr_code, "base64-qr")

    @patch("apps.gateway.services._mercadopago_request")
    def test_create_mercadopago_payment_sends_items_descriptor_and_device_id(self, mercadopago_request):
        mercadopago_request.return_value = {
            "id": "ORD123",
            "transactions": {
                "payments": [
                    {
                        "id": "PAY123",
                        "payment_method": {
                            "qr_code": "pix-code",
                            "qr_code_base64": "base64-qr",
                        },
                    }
                ]
            },
        }

        create_payment(purchase=self.purchase, provider="mercadopago", device_id="device-123")

        kwargs = mercadopago_request.call_args.kwargs
        self.assertEqual(kwargs["extra_headers"]["X-meli-session-id"], "device-123")
        self.assertEqual(kwargs["payload"]["items"][0]["quantity"], 2)
        self.assertEqual(kwargs["payload"]["items"][0]["unit_price"], "10.00")
        self.assertEqual(kwargs["payload"]["items"][0]["title"], self.raffle.title)
        self.assertEqual(kwargs["payload"]["items"][0]["external_code"], f"raffle-{self.raffle.id}")
        self.assertEqual(kwargs["payload"]["transactions"]["payments"][0]["payment_method"]["statement_descriptor"], "MARIA")
        self.assertNotIn("notification_url", kwargs["payload"])


class MercadoPagoWebhookSignatureTests(TestCase):
    def test_validate_mercadopago_signature(self):
        secret = "test-secret"
        payload = {"data": {"id": "12345"}}
        request_id = "req-abc"
        ts = "1710000000"
        manifest = f"id:12345;request-id:{request_id};ts:{ts};"
        signature = hmac.new(secret.encode("utf-8"), manifest.encode("utf-8"), hashlib.sha256).hexdigest()

        with self.settings(MERCADOPAGO_WEBHOOK_SECRET=secret):
            is_valid, metadata = validate_mercadopago_signature(
                payload=payload,
                headers={
                    "x-signature": f"ts={ts},v1={signature}",
                    "x-request-id": request_id,
                },
            )

        self.assertTrue(is_valid)
        self.assertEqual(metadata["data_id"], "12345")

    def test_validate_mercadopago_signature_fails_with_wrong_signature(self):
        with self.settings(MERCADOPAGO_WEBHOOK_SECRET="test-secret"):
            is_valid, metadata = validate_mercadopago_signature(
                payload={"data": {"id": "12345"}},
                headers={
                    "x-signature": "ts=1710000000,v1=invalid",
                    "x-request-id": "req-abc",
                },
            )

        self.assertFalse(is_valid)
        self.assertTrue(metadata["v1_present"])


class MercadoPagoWebhookProcessingTests(TestCase):
    def setUp(self):
        self.raffle = Raffle.objects.create(
            title="Rifa da Maria",
            description="Campanha beneficente",
            beneficiary_name="Maria",
            price_per_number=10,
            total_numbers=10,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=10),
            draw_date=timezone.now() + timedelta(days=11),
        )
        activate_raffle(self.raffle)
        self.purchase = create_purchase(
            raffle_id=self.raffle.id,
            buyer_data={
                "first_name": "APRO",
                "last_name": "Teste",
                "email": "test_user_br@testuser.com",
                "phone": "91999999999",
                "cpf": "12345678909",
            },
            numbers=[1, 2],
        )
        self.payment = Payment.objects.create(
            purchase=self.purchase,
            provider="mercadopago",
            amount=self.purchase.total_amount,
            external_id="ORD123",
            status=Payment.Status.PENDING,
        )

    @patch("apps.gateway.services._mercadopago_request")
    def test_process_webhook_confirms_paid_order(self, mercadopago_request):
        mercadopago_request.return_value = {
            "id": "ORD123",
            "external_reference": str(self.purchase.reference),
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
        secret = "test-secret"
        request_id = "req-abc"
        ts = "1710000000"
        manifest = "id:ORD123;request-id:req-abc;ts:1710000000;"
        signature = hmac.new(secret.encode("utf-8"), manifest.encode("utf-8"), hashlib.sha256).hexdigest()

        with self.settings(MERCADOPAGO_WEBHOOK_SECRET=secret):
            log = process_webhook(
                provider="mercadopago",
                payload={"data": {"id": "ORD123"}},
                headers={
                    "x-signature": f"ts={ts},v1={signature}",
                    "x-request-id": request_id,
                },
                query_params={"data.id": "ORD123", "type": "order"},
            )

        self.assertTrue(log.processed)
        self.purchase.refresh_from_db()
        self.payment.refresh_from_db()
        self.assertEqual(self.purchase.status, Purchase.Status.PAID)
        self.assertEqual(self.purchase.payment_reference, "PAY123")
        self.assertEqual(self.payment.status, Payment.Status.PAID)

    @patch("apps.gateway.services._mercadopago_request")
    def test_process_webhook_cancels_rejected_order(self, mercadopago_request):
        mercadopago_request.return_value = {
            "id": "ORD123",
            "external_reference": str(self.purchase.reference),
            "status": "rejected",
            "transactions": {
                "payments": [
                    {
                        "id": "PAY123",
                        "status": "rejected",
                    }
                ]
            },
        }
        secret = "test-secret"
        request_id = "req-abc"
        ts = "1710000000"
        manifest = "id:ORD123;request-id:req-abc;ts:1710000000;"
        signature = hmac.new(secret.encode("utf-8"), manifest.encode("utf-8"), hashlib.sha256).hexdigest()

        with self.settings(MERCADOPAGO_WEBHOOK_SECRET=secret):
            log = process_webhook(
                provider="mercadopago",
                payload={"data": {"id": "ORD123"}},
                headers={
                    "x-signature": f"ts={ts},v1={signature}",
                    "x-request-id": request_id,
                },
                query_params={"data.id": "ORD123", "type": "order"},
            )

        self.assertTrue(log.processed)
        self.payment.refresh_from_db()
        self.purchase.refresh_from_db()
        self.assertEqual(self.payment.status, Payment.Status.CANCELED)
        self.assertEqual(self.purchase.status, Purchase.Status.RESERVED)

    def test_process_webhook_rejects_unsupported_provider(self):
        with self.assertRaisesMessage(ValidationError, "Webhook provider nao suportado."):
            process_webhook(
                provider="local_pix",
                payload={"payment_id": self.payment.id, "status": Payment.Status.PAID},
                headers={},
                query_params={},
            )

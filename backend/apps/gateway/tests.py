from datetime import timedelta
import hashlib
import hmac

from django.test import TestCase
from django.utils import timezone

from apps.compras.models import Purchase
from apps.compras.services import create_purchase
from apps.rifa.models import Raffle, RaffleNumber
from apps.rifa.services import activate_raffle

from .models import Payment
from .services import confirm_payment, create_payment, validate_mercadopago_signature


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

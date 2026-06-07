from datetime import timedelta
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.gateway.models import Payment
from apps.gateway.services import confirm_payment
from apps.rifa.models import Raffle, RaffleNumber
from apps.rifa.services import activate_raffle

from .models import Purchase, PurchaseEvent
from .serializers import BuyerSerializer
from .services import confirm_purchase_payment, create_purchase, expire_purchase


class PurchaseServiceTests(TestCase):
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
        self.buyer_data = {
            "first_name": "Ana",
            "last_name": "Silva",
            "email": "ana@example.com",
            "phone": "91999999999",
            "cpf": "12345678909",
        }

    @override_settings(RESERVATION_MINUTES=15)
    def test_create_purchase_reserves_numbers(self):
        purchase = create_purchase(raffle_id=self.raffle.id, buyer_data=self.buyer_data, numbers=[1, 2, 3])

        self.assertEqual(purchase.status, Purchase.Status.RESERVED)
        self.assertEqual(purchase.total_amount, 30)
        self.assertEqual(list(purchase.numbers.values_list("number", flat=True)), [1, 2, 3])
        self.assertEqual(
            RaffleNumber.objects.filter(raffle=self.raffle, status=RaffleNumber.Status.RESERVED).count(),
            3,
        )
        event = purchase.events.get(event_type=PurchaseEvent.EventType.RESERVED)
        self.assertEqual(event.source, "api")
        self.assertEqual(event.buyer_name, "Ana Silva")
        self.assertEqual(event.buyer_email, "ana@example.com")
        self.assertEqual(event.numbers_snapshot, [1, 2, 3])
        self.assertEqual(event.metadata["numbers"], [1, 2, 3])

    def test_create_purchase_blocks_duplicate_reserved_number(self):
        create_purchase(raffle_id=self.raffle.id, buyer_data=self.buyer_data, numbers=[1])

        with self.assertRaises(ValidationError):
            create_purchase(raffle_id=self.raffle.id, buyer_data=self.buyer_data, numbers=[1])

    def test_expire_purchase_releases_numbers(self):
        purchase = create_purchase(raffle_id=self.raffle.id, buyer_data=self.buyer_data, numbers=[4, 5])
        purchase.reservation_expires_at = timezone.now() - timedelta(minutes=1)
        purchase.save(update_fields=["reservation_expires_at"])

        expire_purchase(purchase, source="cron", metadata={"reason": "reservation_timeout"})

        purchase.refresh_from_db()
        self.assertEqual(purchase.status, Purchase.Status.EXPIRED)
        self.assertEqual(
            RaffleNumber.objects.filter(number__in=[4, 5], status=RaffleNumber.Status.AVAILABLE).count(),
            2,
        )
        event = purchase.events.get(event_type=PurchaseEvent.EventType.EXPIRED)
        self.assertEqual(event.source, "cron")
        self.assertEqual(event.buyer_cpf, "12345678909")
        self.assertEqual(event.numbers_snapshot, [4, 5])
        self.assertEqual(event.metadata["reason"], "reservation_timeout")

    def test_buyer_serializer_requires_email(self):
        serializer = BuyerSerializer(
            data={
                "full_name": "Ana Maria Silva",
                "phone": "91999999999",
                "cpf": "12345678909",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


class PurchaseLookupApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
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

        self.matching_purchase = create_purchase(
            raffle_id=self.raffle.id,
            buyer_data={
                "first_name": "Ana",
                "last_name": "Silva",
                "email": "ana@example.com",
                "phone": "(91) 99999-1234",
                "cpf": "12345678909",
            },
            numbers=[1, 2],
        )

        self.other_purchase = create_purchase(
            raffle_id=self.raffle.id,
            buyer_data={
                "first_name": "Bruno",
                "last_name": "Souza",
                "email": "bruno@example.com",
                "phone": "(91) 98888-7777",
                "cpf": "98765432100",
            },
            numbers=[3],
        )
        self.other_purchase.status = Purchase.Status.EXPIRED
        self.other_purchase.save(update_fields=["status", "updated_at"])

    def test_lookup_finds_purchase_by_name(self):
        response = self.client.get(f"/api/v1/purchases/lookup/?raffle_id={self.raffle.id}&search=Ana Silva")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["buyer_name"], "Ana Silva")
        self.assertEqual(response.data[0]["numbers"], [1, 2])

    def test_lookup_finds_purchase_by_cpf_digits(self):
        response = self.client.get(f"/api/v1/purchases/lookup/?raffle_id={self.raffle.id}&search=8909")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["buyer_phone"], "91*****34")

    def test_lookup_requires_minimum_search_length(self):
        response = self.client.get(f"/api/v1/purchases/lookup/?raffle_id={self.raffle.id}&search=an")

        self.assertEqual(response.status_code, 400)
        self.assertIn("search", response.data)


class ExpireStalePurchasesCommandTests(TestCase):
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

    @patch("apps.compras.management.commands.expire_stale_purchases.refresh_payment_status")
    def test_command_expires_stale_reserved_purchase_without_paid_status(self, refresh_payment_status_mock):
        purchase = create_purchase(
            raffle_id=self.raffle.id,
            buyer_data={
                "first_name": "Ana",
                "last_name": "Silva",
                "email": "ana@example.com",
                "phone": "91999999999",
                "cpf": "12345678909",
            },
            numbers=[1, 2],
        )
        purchase.reservation_expires_at = timezone.now() - timedelta(minutes=1)
        purchase.save(update_fields=["reservation_expires_at"])

        Payment.objects.create(
            purchase=purchase,
            provider="mercadopago",
            amount=purchase.total_amount,
            status=Payment.Status.PENDING,
            external_id="ORD123",
        )
        refresh_payment_status_mock.side_effect = lambda current_payment, source="system": current_payment

        output = StringIO()
        call_command("expire_stale_purchases", stdout=output)

        purchase.refresh_from_db()
        self.assertEqual(purchase.status, Purchase.Status.EXPIRED)
        self.assertEqual(
            RaffleNumber.objects.filter(raffle=self.raffle, number__in=[1, 2], status=RaffleNumber.Status.AVAILABLE).count(),
            2,
        )
        self.assertIn("1 reservas expiradas", output.getvalue().lower())

    @patch("apps.compras.management.commands.expire_stale_purchases.refresh_payment_status")
    def test_command_keeps_purchase_paid_when_sync_confirms_payment(self, refresh_payment_status_mock):
        purchase = create_purchase(
            raffle_id=self.raffle.id,
            buyer_data={
                "first_name": "Bruno",
                "last_name": "Souza",
                "email": "bruno@example.com",
                "phone": "91988887777",
                "cpf": "98765432100",
            },
            numbers=[3, 4],
        )
        purchase.reservation_expires_at = timezone.now() - timedelta(minutes=1)
        purchase.save(update_fields=["reservation_expires_at"])

        payment = Payment.objects.create(
            purchase=purchase,
            provider="mercadopago",
            amount=purchase.total_amount,
            status=Payment.Status.PENDING,
            external_id="ORD456",
        )

        def sync_as_paid(current_payment, source="system"):
            current_payment.status = Payment.Status.PAID
            current_payment.paid_at = timezone.now()
            current_payment.save(update_fields=["status", "paid_at", "updated_at"])
            confirm_purchase_payment(current_payment.purchase, payment_reference=str(current_payment.id))
            current_payment.refresh_from_db()
            return current_payment

        refresh_payment_status_mock.side_effect = sync_as_paid

        output = StringIO()
        call_command("expire_stale_purchases", stdout=output)

        purchase.refresh_from_db()
        payment.refresh_from_db()
        self.assertEqual(purchase.status, Purchase.Status.PAID)
        self.assertEqual(payment.status, Payment.Status.PAID)
        self.assertEqual(
            RaffleNumber.objects.filter(raffle=self.raffle, number__in=[3, 4], status=RaffleNumber.Status.PAID).count(),
            2,
        )
        self.assertIn("1 compras confirmadas", output.getvalue().lower())
        confirmed_event = purchase.events.get(event_type=PurchaseEvent.EventType.PAYMENT_CONFIRMED)
        self.assertEqual(confirmed_event.buyer_name, "Bruno Souza")
        self.assertEqual(confirmed_event.numbers_snapshot, [3, 4])
        self.assertIn("payment_reference", confirmed_event.metadata)

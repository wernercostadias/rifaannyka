from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.rifa.models import Raffle, RaffleNumber
from apps.rifa.services import activate_raffle

from .models import Purchase
from .serializers import BuyerSerializer
from .services import create_purchase, expire_purchase


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

    def test_create_purchase_blocks_duplicate_reserved_number(self):
        create_purchase(raffle_id=self.raffle.id, buyer_data=self.buyer_data, numbers=[1])

        with self.assertRaises(ValidationError):
            create_purchase(raffle_id=self.raffle.id, buyer_data=self.buyer_data, numbers=[1])

    def test_expire_purchase_releases_numbers(self):
        purchase = create_purchase(raffle_id=self.raffle.id, buyer_data=self.buyer_data, numbers=[4, 5])
        purchase.reservation_expires_at = timezone.now() - timedelta(minutes=1)
        purchase.save(update_fields=["reservation_expires_at"])

        expire_purchase(purchase)

        purchase.refresh_from_db()
        self.assertEqual(purchase.status, Purchase.Status.EXPIRED)
        self.assertEqual(
            RaffleNumber.objects.filter(number__in=[4, 5], status=RaffleNumber.Status.AVAILABLE).count(),
            2,
        )

    def test_buyer_serializer_accepts_full_name_without_email(self):
        serializer = BuyerSerializer(
            data={
                "full_name": "Ana Maria Silva",
                "phone": "91999999999",
                "cpf": "12345678909",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["first_name"], "Ana")
        self.assertEqual(serializer.validated_data["last_name"], "Maria Silva")
        self.assertEqual(serializer.validated_data["email"], "comprador-12345678909@rifa.local")


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

    def test_lookup_finds_purchase_by_phone_digits(self):
        response = self.client.get(f"/api/v1/purchases/lookup/?raffle_id={self.raffle.id}&search=1234")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["buyer_phone"], "(91) 99999-1234")

    def test_lookup_requires_minimum_search_length(self):
        response = self.client.get(f"/api/v1/purchases/lookup/?raffle_id={self.raffle.id}&search=an")

        self.assertEqual(response.status_code, 400)
        self.assertIn("search", response.data)

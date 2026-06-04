from django.test import TestCase
from django.utils import timezone

from apps.compras.models import Buyer, Purchase, PurchaseNumber
from .models import Raffle, RaffleNumber
from .services import activate_raffle
from .serializers import RaffleNumberSerializer


class RaffleServiceTests(TestCase):
    def test_activate_raffle_creates_numbers(self):
        raffle = Raffle.objects.create(
            title="Rifa da Maria",
            description="Campanha beneficente",
            beneficiary_name="Maria",
            goal_amount=50,
            price_per_number=10,
            total_numbers=5,
            start_date=timezone.now(),
            end_date=timezone.now(),
            draw_date=timezone.now(),
        )

        activate_raffle(raffle)

        raffle.refresh_from_db()
        self.assertEqual(raffle.status, Raffle.Status.ACTIVE)
        self.assertEqual(raffle.numbers.count(), 5)
        self.assertEqual(
            list(raffle.numbers.values_list("number", flat=True)),
            [1, 2, 3, 4, 5],
        )
        self.assertTrue(raffle.numbers.filter(status=RaffleNumber.Status.AVAILABLE).exists())

    def test_goal_amount_updates_total_numbers(self):
        raffle = Raffle.objects.create(
            title="Rifa da Maria",
            description="Campanha beneficente",
            beneficiary_name="Maria",
            goal_amount=2500,
            price_per_number=5,
            total_numbers=1,
            start_date=timezone.now(),
            end_date=timezone.now(),
            draw_date=timezone.now(),
        )

        self.assertEqual(raffle.total_numbers, 500)

    def test_paid_number_serializer_includes_buyer_first_name(self):
        raffle = Raffle.objects.create(
            title="Rifa da Maria",
            description="Campanha beneficente",
            beneficiary_name="Maria",
            goal_amount=2500,
            price_per_number=5,
            total_numbers=1,
            start_date=timezone.now(),
            end_date=timezone.now(),
            draw_date=timezone.now(),
            status=Raffle.Status.ACTIVE,
        )
        raffle_number = RaffleNumber.objects.create(
            raffle=raffle,
            number=1,
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
            raffle=raffle,
            buyer=buyer,
            total_amount=5,
            status=Purchase.Status.PAID,
            reservation_expires_at=timezone.now(),
        )
        PurchaseNumber.objects.create(purchase=purchase, raffle_number=raffle_number)

        serializer = RaffleNumberSerializer(
            [raffle_number],
            many=True,
        )

        self.assertEqual(serializer.data[0]["owner_name"], "Annyka")

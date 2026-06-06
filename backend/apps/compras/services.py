from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.rifa.models import Raffle, RaffleNumber

from .models import Buyer, Purchase, PurchaseNumber


def expire_stale_purchases(*, raffle: Raffle, numbers: list[int] | None = None) -> int:
    queryset = (
        Purchase.objects.select_related("raffle")
        .prefetch_related("numbers")
        .filter(
            raffle=raffle,
            status=Purchase.Status.RESERVED,
            reservation_expires_at__lte=timezone.now(),
        )
        .order_by("reservation_expires_at")
    )
    if numbers:
        queryset = queryset.filter(numbers__number__in=numbers).distinct()

    expired = 0
    for purchase in queryset:
        expire_purchase(purchase)
        expired += 1
    return expired


def create_purchase(*, raffle_id: int, buyer_data: dict, numbers: list[int]) -> Purchase:
    if not numbers:
        raise ValidationError({"numbers": "Escolha pelo menos um numero."})

    clean_numbers = sorted(set(numbers))

    with transaction.atomic():
        raffle = Raffle.objects.select_for_update().get(id=raffle_id, status=Raffle.Status.ACTIVE)
        expire_stale_purchases(raffle=raffle, numbers=clean_numbers)
        raffle_numbers = list(
            RaffleNumber.objects.select_for_update()
            .filter(raffle=raffle, number__in=clean_numbers)
            .order_by("number")
        )

        if len(raffle_numbers) != len(clean_numbers):
            raise ValidationError({"numbers": "Um ou mais numeros nao existem nesta rifa."})

        unavailable = [item.number for item in raffle_numbers if item.status != RaffleNumber.Status.AVAILABLE]
        if unavailable:
            raise ValidationError({"numbers": f"Numeros indisponiveis: {', '.join(map(str, unavailable))}."})

        buyer = Buyer.objects.create(**buyer_data)
        total_amount = raffle.price_per_number * len(raffle_numbers)
        purchase = Purchase.objects.create(
            raffle=raffle,
            buyer=buyer,
            total_amount=total_amount,
            status=Purchase.Status.RESERVED,
            reservation_expires_at=timezone.now() + timedelta(minutes=settings.RESERVATION_MINUTES),
        )

        PurchaseNumber.objects.bulk_create(
            [PurchaseNumber(purchase=purchase, raffle_number=raffle_number) for raffle_number in raffle_numbers]
        )

        for raffle_number in raffle_numbers:
            raffle_number.status = RaffleNumber.Status.RESERVED
        RaffleNumber.objects.bulk_update(raffle_numbers, ["status", "updated_at"])

    return purchase


def expire_purchase(purchase: Purchase) -> Purchase:
    if purchase.status != Purchase.Status.RESERVED:
        return purchase
    if purchase.reservation_expires_at > timezone.now():
        return purchase

    with transaction.atomic():
        purchase = Purchase.objects.select_for_update().get(id=purchase.id)
        raffle_numbers = list(purchase.numbers.select_for_update())
        for raffle_number in raffle_numbers:
            if raffle_number.status == RaffleNumber.Status.RESERVED:
                raffle_number.status = RaffleNumber.Status.AVAILABLE
        RaffleNumber.objects.bulk_update(raffle_numbers, ["status", "updated_at"])
        purchase.status = Purchase.Status.EXPIRED
        purchase.save(update_fields=["status", "updated_at"])
    return purchase


def release_purchase(purchase: Purchase, *, status: str = Purchase.Status.CANCELED) -> Purchase:
    if purchase.status != Purchase.Status.RESERVED:
        return purchase

    with transaction.atomic():
        purchase = Purchase.objects.select_for_update().get(id=purchase.id)
        raffle_numbers = list(purchase.numbers.select_for_update())
        for raffle_number in raffle_numbers:
            if raffle_number.status == RaffleNumber.Status.RESERVED:
                raffle_number.status = RaffleNumber.Status.AVAILABLE
        RaffleNumber.objects.bulk_update(raffle_numbers, ["status", "updated_at"])
        purchase.status = status
        purchase.save(update_fields=["status", "updated_at"])
    return purchase


def confirm_purchase_payment(purchase: Purchase, payment_reference: str = "") -> Purchase:
    with transaction.atomic():
        purchase = Purchase.objects.select_for_update().get(id=purchase.id)
        raffle_numbers = list(purchase.numbers.select_for_update())
        for raffle_number in raffle_numbers:
            raffle_number.status = RaffleNumber.Status.PAID
        RaffleNumber.objects.bulk_update(raffle_numbers, ["status", "updated_at"])
        purchase.status = Purchase.Status.PAID
        purchase.payment_reference = payment_reference
        purchase.save(update_fields=["status", "payment_reference", "updated_at"])
    return purchase

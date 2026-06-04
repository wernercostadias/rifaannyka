from django.db import transaction

from .models import Raffle, RaffleNumber


def ensure_raffle_numbers(raffle: Raffle) -> None:
    existing = set(raffle.numbers.values_list("number", flat=True))
    missing = [
        RaffleNumber(raffle=raffle, number=number)
        for number in range(1, raffle.total_numbers + 1)
        if number not in existing
    ]
    if missing:
        RaffleNumber.objects.bulk_create(missing)


def activate_raffle(raffle: Raffle) -> Raffle:
    with transaction.atomic():
        ensure_raffle_numbers(raffle)
        raffle.status = Raffle.Status.ACTIVE
        raffle.save(update_fields=["status", "updated_at"])
    return raffle

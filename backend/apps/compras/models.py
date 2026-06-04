import uuid

from django.db import models

from apps.core.models import BaseModel
from apps.rifa.models import Raffle, RaffleNumber


class Buyer(BaseModel):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    cpf = models.CharField(max_length=14)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Purchase(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        RESERVED = "reserved", "Reservada"
        PAID = "paid", "Paga"
        EXPIRED = "expired", "Expirada"
        CANCELED = "canceled", "Cancelada"

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    raffle = models.ForeignKey(Raffle, on_delete=models.PROTECT, related_name="purchases")
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, related_name="purchases")
    numbers = models.ManyToManyField(RaffleNumber, through="PurchaseNumber", related_name="purchases")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reservation_expires_at = models.DateTimeField()
    payment_reference = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return str(self.reference)


class PurchaseNumber(BaseModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_numbers")
    raffle_number = models.ForeignKey(RaffleNumber, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["purchase", "raffle_number"], name="unique_purchase_raffle_number"),
        ]

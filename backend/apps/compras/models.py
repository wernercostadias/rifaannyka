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


class PurchaseEvent(BaseModel):
    class EventType(models.TextChoices):
        RESERVED = "reserved", "Reserva criada"
        PAYMENT_CHECKED = "payment_checked", "Pagamento consultado"
        PAYMENT_CONFIRMED = "payment_confirmed", "Pagamento confirmado"
        EXPIRED = "expired", "Reserva expirada"
        RELEASED = "released", "Reserva liberada"
        SYNC_FAILED = "sync_failed", "Falha de sincronizacao"

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="events")
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, related_name="purchase_events")
    event_type = models.CharField(max_length=40, choices=EventType.choices)
    source = models.CharField(max_length=40, default="system")
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    message = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    numbers_snapshot = models.JSONField(default=list, blank=True)
    buyer_name = models.CharField(max_length=241)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=30)
    buyer_cpf = models.CharField(max_length=14)

    def __str__(self):
        return f"{self.purchase.reference} - {self.event_type}"

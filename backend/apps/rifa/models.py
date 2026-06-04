from decimal import Decimal, ROUND_CEILING

from django.db import models
from django.db.models import Sum

from apps.core.models import BaseModel


class Raffle(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Rascunho"
        ACTIVE = "active", "Ativa"
        FINISHED = "finished", "Finalizada"
        CANCELED = "canceled", "Cancelada"

    title = models.CharField(max_length=180)
    description = models.TextField()
    beneficiary_name = models.CharField(max_length=180)
    goal_description = models.TextField(blank=True)
    image = models.ImageField(upload_to="raffles/", blank=True, null=True)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=2500)
    price_per_number = models.DecimalField(max_digits=10, decimal_places=2)
    total_numbers = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    draw_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    winner_number = models.PositiveIntegerField(blank=True, null=True)
    winner_name = models.CharField(max_length=180, blank=True)

    def __str__(self):
        return self.title

    def sync_total_numbers_with_goal(self):
        if not self.price_per_number:
            return

        goal_amount = Decimal(self.goal_amount or 0)
        price_per_number = Decimal(self.price_per_number or 0)
        if goal_amount <= 0 or price_per_number <= 0:
            return

        required_numbers = int((goal_amount / price_per_number).to_integral_value(rounding=ROUND_CEILING))
        self.total_numbers = max(required_numbers, 1)

    @property
    def paid_numbers_count(self) -> int:
        return self.numbers.filter(status=RaffleNumber.Status.PAID).count()

    @property
    def raised_amount(self) -> Decimal:
        total = self.purchases.filter(status="paid").aggregate(total=Sum("total_amount"))["total"]
        return total or Decimal("0.00")

    @property
    def progress_percentage(self) -> Decimal:
        if not self.goal_amount:
            return Decimal("0.00")
        return min((self.raised_amount / self.goal_amount) * Decimal("100"), Decimal("100.00"))

    def save(self, *args, **kwargs):
        self.sync_total_numbers_with_goal()
        super().save(*args, **kwargs)


class RaffleNumber(BaseModel):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Disponivel"
        RESERVED = "reserved", "Reservado"
        PAID = "paid", "Pago"
        CANCELED = "canceled", "Cancelado"

    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name="numbers")
    number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["raffle", "number"], name="unique_raffle_number"),
        ]
        ordering = ["number"]

    def __str__(self):
        return f"{self.raffle} - {self.number}"

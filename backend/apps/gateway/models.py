from django.db import models

from apps.compras.models import Purchase
from apps.core.models import BaseModel


class Payment(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        PAID = "paid", "Pago"
        FAILED = "failed", "Falhou"
        CANCELED = "canceled", "Cancelado"
        REFUNDED = "refunded", "Reembolsado"

    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, related_name="payments")
    provider = models.CharField(max_length=60, default="local_pix")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    external_id = models.CharField(max_length=180, blank=True)
    qr_code = models.TextField(blank=True)
    qr_code_text = models.TextField(blank=True)
    paid_at = models.DateTimeField(blank=True, null=True)


class PaymentWebhookLog(BaseModel):
    provider = models.CharField(max_length=60)
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

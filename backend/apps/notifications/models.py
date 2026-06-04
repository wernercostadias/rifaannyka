from django.db import models

from apps.compras.models import Buyer, Purchase
from apps.core.models import BaseModel


class NotificationLog(BaseModel):
    class Channel(models.TextChoices):
        EMAIL = "email", "E-mail"
        WHATSAPP = "whatsapp", "WhatsApp"
        SMS = "sms", "SMS"

    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, related_name="notification_logs")
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, related_name="notification_logs")
    channel = models.CharField(max_length=20, choices=Channel.choices)
    status = models.CharField(max_length=30, default="pending")
    payload = models.JSONField(default=dict)
    sent_at = models.DateTimeField(blank=True, null=True)

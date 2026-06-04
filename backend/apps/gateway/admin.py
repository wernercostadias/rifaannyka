from django.contrib import admin

from .models import Payment, PaymentWebhookLog


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "purchase", "provider", "amount", "status", "paid_at")
    list_filter = ("provider", "status")
    search_fields = ("purchase__reference", "external_id")


@admin.register(PaymentWebhookLog)
class PaymentWebhookLogAdmin(admin.ModelAdmin):
    list_display = ("provider", "received_at", "processed")
    list_filter = ("provider", "processed")

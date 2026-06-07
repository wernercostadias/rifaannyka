from django.contrib import admin, messages
from rest_framework.exceptions import ValidationError

from .models import Payment, PaymentWebhookLog
from .services import refresh_payment_status


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "purchase", "provider", "amount", "status", "external_id", "paid_at")
    list_filter = ("provider", "status")
    search_fields = ("purchase__reference", "external_id")
    actions = ("sync_mercadopago_payments",)

    @admin.action(description="Sincronizar status no Mercado Pago")
    def sync_mercadopago_payments(self, request, queryset):
        synced = 0
        failed = 0

        for payment in queryset.select_related("purchase"):
            if payment.provider != "mercadopago":
                continue
            try:
                refresh_payment_status(payment, source="admin")
                synced += 1
            except ValidationError as exc:
                failed += 1
                self.message_user(
                    request,
                    f"Falha ao sincronizar pagamento {payment.id}: {exc.detail}",
                    level=messages.WARNING,
                )

        if synced:
            self.message_user(request, f"{synced} pagamento(s) sincronizado(s) com sucesso.")
        if failed:
            self.message_user(
                request,
                f"{failed} pagamento(s) falharam na sincronizacao.",
                level=messages.WARNING,
            )


@admin.register(PaymentWebhookLog)
class PaymentWebhookLogAdmin(admin.ModelAdmin):
    list_display = ("provider", "received_at", "processed")
    list_filter = ("provider", "processed")

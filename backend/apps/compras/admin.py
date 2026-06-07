from django.contrib import admin
from django.utils.html import format_html
import json

from .models import Buyer, Purchase, PurchaseEvent, PurchaseNumber


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "cpf", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone", "cpf")


class PurchaseNumberInline(admin.TabularInline):
    model = PurchaseNumber
    extra = 0
    readonly_fields = ("raffle_number",)


class PurchaseEventInline(admin.TabularInline):
    model = PurchaseEvent
    extra = 0
    can_delete = False
    readonly_fields = (
        "created_at",
        "event_type",
        "source",
        "old_status",
        "new_status",
        "numbers_snapshot",
        "buyer_name",
        "buyer_email",
        "buyer_phone",
        "buyer_cpf",
        "message",
        "formatted_metadata",
    )

    fields = (
        "created_at",
        "event_type",
        "source",
        "old_status",
        "new_status",
        "numbers_snapshot",
        "buyer_name",
        "buyer_email",
        "buyer_phone",
        "buyer_cpf",
        "message",
        "formatted_metadata",
    )

    def formatted_metadata(self, obj):
        if not obj.metadata:
            return "-"

        pretty = json.dumps(obj.metadata, ensure_ascii=False, indent=2, sort_keys=True)
        return format_html("<pre style='white-space: pre-wrap; margin: 0; font-size: 12px;'>{}</pre>", pretty)

    formatted_metadata.short_description = "Metadata"


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("reference", "buyer", "raffle", "total_amount", "status", "reservation_expires_at")
    list_filter = ("status", "raffle")
    search_fields = ("reference", "buyer__first_name", "buyer__last_name", "buyer__email", "buyer__phone", "buyer__cpf")
    inlines = [PurchaseNumberInline, PurchaseEventInline]

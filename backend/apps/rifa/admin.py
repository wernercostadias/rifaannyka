from django.contrib import admin
from django.db.models import Prefetch

from apps.compras.models import PurchaseNumber

from .models import Raffle, RaffleNumber


@admin.register(Raffle)
class RaffleAdmin(admin.ModelAdmin):
    list_display = ("title", "beneficiary_name", "goal_amount", "price_per_number", "total_numbers", "status", "draw_date")
    list_filter = ("status", "draw_date")
    search_fields = ("title", "beneficiary_name")


@admin.register(RaffleNumber)
class RaffleNumberAdmin(admin.ModelAdmin):
    list_display = ("raffle", "number", "status", "buyer_name", "buyer_phone", "purchase_reference")
    list_filter = ("status", "raffle")
    search_fields = (
        "raffle__title",
        "number",
        "purchases__buyer__first_name",
        "purchases__buyer__last_name",
        "purchases__buyer__cpf",
    )

    def get_queryset(self, request):
        purchase_number_qs = PurchaseNumber.objects.select_related("purchase__buyer").order_by("-created_at")
        return (
            super()
            .get_queryset(request)
            .prefetch_related(Prefetch("purchasenumber_set", queryset=purchase_number_qs))
        )

    def _latest_purchase(self, obj):
        purchase_number = next(iter(obj.purchasenumber_set.all()), None)
        return purchase_number.purchase if purchase_number else None

    def buyer_name(self, obj):
        purchase = self._latest_purchase(obj)
        if not purchase:
            return "-"
        full_name = f"{purchase.buyer.first_name} {purchase.buyer.last_name}".strip()
        return full_name or purchase.buyer.first_name

    buyer_name.short_description = "Comprador"

    def buyer_phone(self, obj):
        purchase = self._latest_purchase(obj)
        if not purchase:
            return "-"
        phone = "".join(char for char in purchase.buyer.phone if char.isdigit())
        if len(phone) < 4:
            return "***"
        return f"{phone[:2]}*****{phone[-2:]}"

    buyer_phone.short_description = "Celular"

    def purchase_reference(self, obj):
        purchase = self._latest_purchase(obj)
        if not purchase:
            return "-"
        return str(purchase.reference)

    purchase_reference.short_description = "Compra"

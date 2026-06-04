from django.contrib import admin

from .models import Buyer, Purchase, PurchaseNumber


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "cpf", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone", "cpf")


class PurchaseNumberInline(admin.TabularInline):
    model = PurchaseNumber
    extra = 0
    readonly_fields = ("raffle_number",)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("reference", "buyer", "raffle", "total_amount", "status", "reservation_expires_at")
    list_filter = ("status", "raffle")
    search_fields = ("reference", "buyer__first_name", "buyer__last_name", "buyer__email", "buyer__phone", "buyer__cpf")
    inlines = [PurchaseNumberInline]

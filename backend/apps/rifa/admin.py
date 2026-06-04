from django.contrib import admin

from .models import Raffle, RaffleNumber


@admin.register(Raffle)
class RaffleAdmin(admin.ModelAdmin):
    list_display = ("title", "beneficiary_name", "goal_amount", "price_per_number", "total_numbers", "status", "draw_date")
    list_filter = ("status", "draw_date")
    search_fields = ("title", "beneficiary_name")


@admin.register(RaffleNumber)
class RaffleNumberAdmin(admin.ModelAdmin):
    list_display = ("raffle", "number", "status")
    list_filter = ("status", "raffle")
    search_fields = ("raffle__title", "number")

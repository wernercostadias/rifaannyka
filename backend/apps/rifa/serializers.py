from rest_framework import serializers

from .models import Raffle, RaffleNumber


class RaffleListSerializer(serializers.ModelSerializer):
    sold_count = serializers.IntegerField(read_only=True)
    goal_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    raised_amount = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Raffle
        fields = [
            "id",
            "title",
            "description",
            "beneficiary_name",
            "image",
            "goal_amount",
            "price_per_number",
            "total_numbers",
            "draw_date",
            "status",
            "sold_count",
            "raised_amount",
            "progress_percentage",
        ]

    def get_raised_amount(self, obj):
        return f"{obj.raised_amount:.2f}"

    def get_progress_percentage(self, obj):
        return f"{obj.progress_percentage:.2f}"


class RaffleDetailSerializer(RaffleListSerializer):
    class Meta(RaffleListSerializer.Meta):
        fields = RaffleListSerializer.Meta.fields + [
            "goal_description",
            "start_date",
            "end_date",
            "winner_number",
            "winner_name",
        ]


class RaffleNumberSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = RaffleNumber
        fields = ["id", "number", "status", "owner_name"]

    def get_owner_name(self, obj):
        if obj.status != RaffleNumber.Status.PAID:
            return ""

        paid_purchases = getattr(obj, "paid_purchases", None)
        purchase = paid_purchases[0] if paid_purchases else obj.purchases.filter(status="paid").select_related("buyer").order_by("-created_at").first()
        if purchase is None:
            return ""

        return purchase.buyer.first_name.strip()

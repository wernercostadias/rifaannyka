from rest_framework import serializers

from .models import Buyer, Purchase
from .services import create_purchase


class BuyerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    cpf = serializers.CharField(max_length=14)

    class Meta:
        model = Buyer
        fields = ["full_name", "first_name", "last_name", "email", "phone", "cpf"]

    def validate(self, attrs):
        full_name = (attrs.pop("full_name", "") or "").strip()
        first_name = (attrs.get("first_name") or "").strip()
        last_name = (attrs.get("last_name") or "").strip()

        if full_name:
            name_parts = [part for part in full_name.split() if part]
            if not name_parts:
                raise serializers.ValidationError({"full_name": "Informe o nome completo."})
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:])

        if not first_name:
            raise serializers.ValidationError({"full_name": "Informe o nome completo."})

        attrs["first_name"] = first_name
        attrs["last_name"] = last_name

        email = (attrs.get("email") or "").strip()
        if not email:
            cpf_digits = "".join(char for char in attrs.get("cpf", "") if char.isdigit())
            attrs["email"] = f"comprador-{cpf_digits}@testuser.com"

        return attrs

    def validate_cpf(self, value):
        digits = "".join(char for char in value if char.isdigit())
        if len(digits) != 11:
            raise serializers.ValidationError("Informe um CPF com 11 digitos.")
        return digits


class PurchaseCreateSerializer(serializers.Serializer):
    raffle_id = serializers.IntegerField()
    buyer = BuyerSerializer()
    numbers = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=False)
    payment_provider = serializers.CharField(required=False, allow_blank=True)
    device_id = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        return create_purchase(
            raffle_id=validated_data["raffle_id"],
            buyer_data=validated_data["buyer"],
            numbers=validated_data["numbers"],
        )


class PurchaseSerializer(serializers.ModelSerializer):
    buyer = BuyerSerializer()
    numbers = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = [
            "reference",
            "raffle",
            "buyer",
            "numbers",
            "total_amount",
            "status",
            "reservation_expires_at",
            "payment_reference",
        ]

    def get_numbers(self, obj):
        return list(obj.numbers.order_by("number").values_list("number", flat=True))


class PublicPurchaseSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField()
    buyer_phone = serializers.SerializerMethodField()
    numbers = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ["buyer_name", "buyer_phone", "numbers", "status", "created_at"]

    def get_buyer_name(self, obj):
        if obj.buyer.last_name:
            return f"{obj.buyer.first_name} {obj.buyer.last_name[:1]}."
        return obj.buyer.first_name

    def get_buyer_phone(self, obj):
        phone = "".join(char for char in obj.buyer.phone if char.isdigit())
        if len(phone) < 4:
            return "***"
        return f"{phone[:2]}*****{phone[-2:]}"

    def get_numbers(self, obj):
        return list(obj.numbers.order_by("number").values_list("number", flat=True))


class PurchaseLookupSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField()
    buyer_phone = serializers.CharField(source="buyer.phone")
    numbers = serializers.SerializerMethodField()
    status_label = serializers.CharField(source="get_status_display")

    class Meta:
        model = Purchase
        fields = ["reference", "buyer_name", "buyer_phone", "numbers", "status", "status_label", "created_at"]

    def get_buyer_name(self, obj):
        full_name = f"{obj.buyer.first_name} {obj.buyer.last_name}".strip()
        return full_name or obj.buyer.first_name

    def get_numbers(self, obj):
        return list(obj.numbers.order_by("number").values_list("number", flat=True))

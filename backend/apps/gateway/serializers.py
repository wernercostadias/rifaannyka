from rest_framework import serializers

from apps.compras.models import Purchase

from .models import Payment
from .services import create_payment


class PaymentCreateSerializer(serializers.Serializer):
    purchase_reference = serializers.UUIDField()
    provider = serializers.CharField(default="local_pix", required=False)

    def create(self, validated_data):
        purchase = Purchase.objects.get(reference=validated_data["purchase_reference"])
        return create_payment(purchase=purchase, provider=validated_data.get("provider", "local_pix"))


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "purchase",
            "provider",
            "amount",
            "status",
            "external_id",
            "qr_code",
            "qr_code_text",
            "paid_at",
        ]

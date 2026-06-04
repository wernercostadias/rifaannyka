from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Purchase
from .serializers import PublicPurchaseSerializer, PurchaseCreateSerializer, PurchaseSerializer
from .services import expire_purchase


class PurchaseViewSet(GenericViewSet):
    lookup_field = "reference"
    queryset = Purchase.objects.select_related("buyer", "raffle").prefetch_related("numbers")

    def get_serializer_class(self):
        if self.action == "create":
            return PurchaseCreateSerializer
        return PurchaseSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchase = serializer.save()
        return Response(PurchaseSerializer(purchase).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, reference=None):
        purchase = self.get_object()
        expire_purchase(purchase)
        purchase.refresh_from_db()
        return Response(PurchaseSerializer(purchase).data)

    @action(detail=True, methods=["post"], url_path="cancel-expired")
    def cancel_expired(self, request, reference=None):
        purchase = expire_purchase(self.get_object())
        return Response(PurchaseSerializer(purchase).data)

    @action(detail=False, methods=["get"], url_path="latest")
    def latest(self, request):
        raffle_id = request.query_params.get("raffle_id")
        queryset = self.get_queryset().filter(status__in=[Purchase.Status.RESERVED, Purchase.Status.PAID])
        if raffle_id:
            queryset = queryset.filter(raffle_id=raffle_id)
        queryset = queryset.order_by("-created_at")[:8]
        return Response(PublicPurchaseSerializer(queryset, many=True).data)

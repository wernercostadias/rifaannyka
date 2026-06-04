from django.db.models import Count, Prefetch, Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.compras.models import Purchase
from .models import Raffle, RaffleNumber
from .serializers import RaffleDetailSerializer, RaffleListSerializer, RaffleNumberSerializer


class RaffleViewSet(ReadOnlyModelViewSet):
    queryset = Raffle.objects.annotate(
        sold_count=Count("numbers", filter=Q(numbers__status=RaffleNumber.Status.PAID))
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RaffleDetailSerializer
        return RaffleListSerializer

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        raffle = self.get_queryset().filter(status=Raffle.Status.ACTIVE).order_by("-created_at").first()
        if raffle is None:
            return Response(None, status=404)
        return Response(RaffleDetailSerializer(raffle, context={"request": request}).data)

    @action(detail=True, methods=["get"], url_path="numbers")
    def numbers(self, request, pk=None):
        raffle = self.get_object()
        numbers = raffle.numbers.prefetch_related(
            Prefetch(
                "purchases",
                queryset=Purchase.objects.filter(status=Purchase.Status.PAID)
                .select_related("buyer")
                .order_by("-created_at"),
                to_attr="paid_purchases",
            )
        )
        serializer = RaffleNumberSerializer(numbers, many=True)
        return Response(serializer.data)

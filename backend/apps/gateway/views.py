from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.compras.serializers import PurchaseSerializer

from .models import Payment
from .serializers import PaymentCreateSerializer, PaymentSerializer
from .services import confirm_payment, process_webhook, refresh_payment_status


class PaymentViewSet(GenericViewSet):
    queryset = Payment.objects.select_related("purchase")

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer
        return PaymentSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        return Response(PaymentSerializer(self.get_object()).data)

    @action(detail=True, methods=["get"], url_path="status")
    def status_view(self, request, pk=None):
        payment = refresh_payment_status(self.get_object())
        return Response(
            {
                "payment": PaymentSerializer(payment).data,
                "purchase": PurchaseSerializer(payment.purchase).data,
            }
        )

    @action(detail=True, methods=["post"], url_path="confirm-local")
    def confirm_local(self, request, pk=None):
        payment = confirm_payment(self.get_object())
        return Response(PaymentSerializer(payment).data)

    @action(detail=False, methods=["post"], url_path=r"webhook/(?P<provider>[^/.]+)")
    def webhook(self, request, provider=None):
        log = process_webhook(
            provider=provider,
            payload=request.data,
            headers={key.lower(): value for key, value in request.headers.items()},
            query_params=dict(request.query_params),
        )
        return Response({"processed": log.processed})

    def get_permissions(self):
        if self.action == "webhook":
            return [AllowAny()]
        return super().get_permissions()

from django.conf import settings
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.compras.serializers import PurchaseSerializer

from .models import Payment
from .serializers import PaymentCreateSerializer, PaymentSerializer
from .services import confirm_payment, process_webhook, refresh_payment_status


class PaymentViewSet(GenericViewSet):
    queryset = Payment.objects.select_related("purchase")

    def _get_scoped_payment(self):
        payment = self.get_object()
        purchase_reference = (self.request.query_params.get("purchase_reference") or "").strip()

        if not purchase_reference or str(payment.purchase.reference) != purchase_reference:
            raise Http404

        return payment

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
        return Response(PaymentSerializer(self._get_scoped_payment()).data)

    @action(detail=True, methods=["get"], url_path="status")
    def status_view(self, request, pk=None):
        payment = refresh_payment_status(self._get_scoped_payment())
        return Response(
            {
                "payment": PaymentSerializer(payment).data,
                "purchase": PurchaseSerializer(payment.purchase).data,
            }
        )

    @action(detail=True, methods=["post"], url_path="confirm-local")
    def confirm_local(self, request, pk=None):
        if not settings.DEBUG:
            raise Http404
        payment = confirm_payment(self._get_scoped_payment())
        return Response(PaymentSerializer(payment).data)

    @action(detail=False, methods=["post"], url_path=r"webhook/(?P<provider>[^/.]+)")
    def webhook(self, request, provider=None):
        if provider != "mercadopago":
            raise ValidationError({"provider": "Webhook nao suportado."})
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

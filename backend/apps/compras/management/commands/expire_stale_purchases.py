from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.compras.models import Purchase
from apps.compras.services import expire_purchase
from apps.gateway.models import Payment
from apps.gateway.services import refresh_payment_status


class Command(BaseCommand):
    help = "Sincroniza pagamentos pendentes e expira reservas vencidas que continuarem sem pagamento."

    def handle(self, *args, **options):
        now = timezone.now()
        stale_purchases = list(
            Purchase.objects.filter(
                status=Purchase.Status.RESERVED,
                reservation_expires_at__lte=now,
            ).order_by("reservation_expires_at")
        )

        synced_payments = 0
        expired_purchases = 0
        confirmed_purchases = 0

        for purchase in stale_purchases:
            pending_payments = list(
                Payment.objects.filter(
                    purchase=purchase,
                    status=Payment.Status.PENDING,
                ).order_by("-created_at")
            )

            for payment in pending_payments:
                try:
                    refreshed = refresh_payment_status(payment)
                    synced_payments += 1
                    refreshed.purchase.refresh_from_db()
                    if refreshed.purchase.status == Purchase.Status.PAID:
                        confirmed_purchases += 1
                        break
                except ValidationError as exc:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Falha ao sincronizar pagamento {payment.id}: {exc.detail}"
                        )
                    )

            purchase.refresh_from_db()
            if purchase.status == Purchase.Status.RESERVED and purchase.reservation_expires_at <= now:
                expire_purchase(purchase)
                expired_purchases += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Resumo: "
                f"{len(stale_purchases)} reservas verificadas | "
                f"{synced_payments} pagamentos consultados | "
                f"{confirmed_purchases} compras confirmadas | "
                f"{expired_purchases} reservas expiradas"
            )
        )

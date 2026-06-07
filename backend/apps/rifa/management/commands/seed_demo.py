from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.rifa.models import Raffle
from apps.rifa.services import activate_raffle


class Command(BaseCommand):
    help = "Cria uma rifa demo ativa com meta de R$ 3.000,00."

    def handle(self, *args, **options):
        now = timezone.now()
        raffle, created = Raffle.objects.update_or_create(
            title="Rifa Estudantil da Annyka",
            defaults={
                "description": "Sua ajuda transforma sonhos em conquistas.",
                "beneficiary_name": "Annyka",
                "goal_description": (
                    "Rifa estudantil para ajudar a Annyka na compra de um notebook "
                    "essencial para seus estudos e para o estagio na area do curso "
                    "de especializacao no IEMA."
                ),
                "goal_amount": 3500,
                "price_per_number": 5,
                "total_numbers": 700,
                "start_date": now,
                "end_date": now + timedelta(days=30),
                "draw_date": now + timedelta(days=31),
                "status": Raffle.Status.DRAFT,
            },
        )
        activate_raffle(raffle)

        action = "criada" if created else "atualizada"
        self.stdout.write(self.style.SUCCESS(f"Rifa demo {action}: {raffle.title} ({raffle.total_numbers} numeros)."))

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rifa", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="raffle",
            name="goal_amount",
            field=models.DecimalField(decimal_places=2, default=2500, max_digits=10),
        ),
    ]

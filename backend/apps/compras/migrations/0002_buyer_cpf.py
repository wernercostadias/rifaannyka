from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("compras", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="buyer",
            name="cpf",
            field=models.CharField(default="", max_length=14),
            preserve_default=False,
        ),
    ]

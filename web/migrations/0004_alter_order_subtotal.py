# Generated by Django 5.0.1 on 2024-03-23 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0003_alter_order_payable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="subtotal",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0.0, max_digits=10, null=True
            ),
        ),
    ]

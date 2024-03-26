# Generated by Django 5.0.1 on 2024-03-25 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0006_alter_order_payment_method"),
    ]

    operations = [
        migrations.CreateModel(
            name="Slider",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.TextField()),
                ("background_image", models.ImageField(upload_to="slider")),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
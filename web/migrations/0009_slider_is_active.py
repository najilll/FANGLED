# Generated by Django 5.0.1 on 2024-03-25 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0008_alter_slider_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="slider",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]

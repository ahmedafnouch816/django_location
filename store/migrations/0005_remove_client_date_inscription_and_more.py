# Generated by Django 5.1.1 on 2024-09-17 14:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_remove_vehicule_photo"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(model_name="client", name="date_inscription",),
        migrations.AlterField(
            model_name="client",
            name="permis_conduire",
            field=models.FileField(blank=True, null=True, upload_to="permis/"),
        ),
        migrations.AlterField(
            model_name="client",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]

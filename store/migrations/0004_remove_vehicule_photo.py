# Generated by Django 5.1.1 on 2024-09-16 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_vehicule_remove_product_category_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="vehicule", name="photo",),
    ]
# Generated by Django 5.1.5 on 2025-04-17 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_order_orderitem"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="billing_address",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="billing_address",
                to="users.address",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="shipping_address",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="shipping_address",
                to="users.address",
            ),
        ),
    ]

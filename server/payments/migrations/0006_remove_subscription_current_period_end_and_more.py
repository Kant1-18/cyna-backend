# Generated by Django 5.1.5 on 2025-05-31 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0005_remove_subscription_stripe_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="current_period_end",
        ),
        migrations.RemoveField(
            model_name="subscription",
            name="current_period_start",
        ),
        migrations.AddField(
            model_name="subscriptionitem",
            name="current_period_end",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="subscriptionitem",
            name="current_period_start",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

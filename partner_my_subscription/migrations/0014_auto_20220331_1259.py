# Generated by Django 3.1.4 on 2022-03-31 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_my_subscription', '0013_partner_recharge_history_gst_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner_recharge_history',
            name='per_url_cost',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='partner_subscriptions',
            name='per_url_cost',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

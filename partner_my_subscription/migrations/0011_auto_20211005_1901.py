# Generated by Django 3.1.4 on 2021-10-05 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_my_subscription', '0010_partner_subscriptions_recharge_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner_subscriptions',
            name='b_transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='partner_subscriptions',
            name='check_no',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

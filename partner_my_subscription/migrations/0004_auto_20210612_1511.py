# Generated by Django 3.1.4 on 2021-06-12 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_my_subscription', '0003_auto_20210612_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner_bulk_sms_subscriptions',
            name='payu_transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='partner_bulk_sms_subscriptions',
            name='transcation_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='partner_recharge_history',
            name='payu_transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='partner_recharge_history',
            name='transcation_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='partner_subscriptions',
            name='payu_transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='partner_subscriptions',
            name='transcation_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

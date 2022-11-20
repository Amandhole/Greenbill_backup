# Generated by Django 3.1.4 on 2021-01-29 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_subscription', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchant_subscriptions',
            name='sms_count',
        ),
        migrations.RemoveField(
            model_name='recharge_history',
            name='is_addons',
        ),
        migrations.RemoveField(
            model_name='recharge_history',
            name='sms_count',
        ),
        migrations.AddField(
            model_name='merchant_subscriptions',
            name='digital_bill',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='merchant_subscriptions',
            name='per_bill_cost',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='merchant_subscriptions',
            name='total_amount_avilable',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recharge_history',
            name='digital_bill',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recharge_history',
            name='per_bill_cost',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recharge_history',
            name='cost',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

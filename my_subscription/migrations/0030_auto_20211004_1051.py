# Generated by Django 3.1.4 on 2021-10-04 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_subscription', '0029_sent_bill_history_is_exe'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant_subscriptions',
            name='merchant_business_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recharge_history',
            name='merchant_business_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

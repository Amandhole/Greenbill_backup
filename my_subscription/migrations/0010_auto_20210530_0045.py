# Generated by Django 3.1.4 on 2021-05-29 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_subscription', '0009_auto_20210530_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant_subscriptions',
            name='valid_for_month',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recharge_history',
            name='valid_for_month',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
# Generated by Django 3.1.4 on 2021-01-29 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_subscription', '0002_auto_20210129_0536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recharge_history',
            name='merchant_id',
        ),
        migrations.RemoveField(
            model_name='recharge_history',
            name='subscription_plan_id',
        ),
        migrations.DeleteModel(
            name='merchant_subscriptions',
        ),
        migrations.DeleteModel(
            name='recharge_history',
        ),
    ]

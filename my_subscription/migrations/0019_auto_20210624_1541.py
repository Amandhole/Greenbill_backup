# Generated by Django 3.1.4 on 2021-06-24 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_subscription', '0018_auto_20210614_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant_subscriptions',
            name='bill_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='merchant_subscriptions',
            name='invoice_no',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
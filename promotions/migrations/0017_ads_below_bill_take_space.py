# Generated by Django 3.1.4 on 2021-08-19 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0016_ads_below_bill_received_cash_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads_below_bill',
            name='take_space',
            field=models.BooleanField(default=False, null=True),
        ),
    ]

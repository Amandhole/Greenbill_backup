# Generated by Django 3.1.4 on 2022-01-19 10:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner_coupon', '0033_auto_20220119_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemownercouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 19, 16, 28, 10, 347251)),
        ),
    ]

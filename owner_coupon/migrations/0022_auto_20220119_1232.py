# Generated by Django 3.1.4 on 2022-01-19 07:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner_coupon', '0021_auto_20211231_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemownercouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 19, 12, 32, 54, 511014)),
        ),
    ]
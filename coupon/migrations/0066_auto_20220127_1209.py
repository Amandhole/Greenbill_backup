# Generated by Django 3.1.4 on 2022-01-27 06:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0065_auto_20220125_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 27, 12, 9, 20, 931555)),
        ),
    ]

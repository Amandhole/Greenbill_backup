# Generated by Django 3.1.4 on 2022-01-19 07:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0046_auto_20220119_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 19, 13, 1, 4, 527123)),
        ),
    ]

# Generated by Django 3.1.4 on 2022-04-15 08:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner_coupon', '0045_auto_20220127_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemownercouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 15, 14, 0, 37, 672068)),
        ),
    ]

# Generated by Django 3.1.4 on 2021-12-20 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner_coupon', '0011_auto_20211218_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemownercouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 20, 16, 56, 8, 254476)),
        ),
    ]

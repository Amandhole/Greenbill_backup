# Generated by Django 3.1.4 on 2022-01-25 10:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0062_auto_20220125_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 25, 16, 4, 48, 913471)),
        ),
    ]

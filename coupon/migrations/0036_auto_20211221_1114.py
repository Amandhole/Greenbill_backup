# Generated by Django 3.1.4 on 2021-12-21 05:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0035_auto_20211220_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 21, 11, 14, 11, 536708)),
        ),
    ]
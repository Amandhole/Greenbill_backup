# Generated by Django 3.1.4 on 2021-12-22 06:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0038_auto_20211222_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 22, 12, 8, 19, 145588)),
        ),
    ]
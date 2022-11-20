# Generated by Django 3.1.4 on 2021-09-07 06:27

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0028_auto_20210827_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponmodel',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 7, 11, 57, 6, 888906)),
        ),
    ]

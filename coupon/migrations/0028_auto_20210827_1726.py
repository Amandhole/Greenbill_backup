# Generated by Django 3.1.4 on 2021-08-27 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0027_auto_20210827_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponmodel',
            name='total_customers',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 27, 17, 26, 55, 922163)),
        ),
    ]

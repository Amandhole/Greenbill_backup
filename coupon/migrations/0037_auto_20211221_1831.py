# Generated by Django 3.1.4 on 2021-12-21 13:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0036_auto_20211221_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 21, 18, 31, 3, 245354)),
        ),
    ]
# Generated by Django 3.1.4 on 2021-03-25 10:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0020_auto_20210325_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponmodel',
            name='amount_in',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 25, 15, 46, 57, 807481)),
        ),
    ]

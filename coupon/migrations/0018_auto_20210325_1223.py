# Generated by Django 3.1.4 on 2021-03-25 06:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0017_auto_20210325_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponmodel',
            name='valid_from',
            field=models.DateField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='couponmodel',
            name='valid_through',
            field=models.DateField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 25, 12, 23, 31, 905748)),
        ),
    ]
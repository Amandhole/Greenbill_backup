# Generated by Django 3.1.4 on 2021-12-11 06:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner_coupon', '0007_auto_20211008_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemownercouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 11, 11, 56, 38, 96711)),
        ),
    ]
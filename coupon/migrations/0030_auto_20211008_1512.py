# Generated by Django 3.1.4 on 2021-10-08 09:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0029_auto_20210907_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemcouponmodel',
            name='coupon_redeem_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 8, 15, 12, 7, 392003)),
        ),
    ]

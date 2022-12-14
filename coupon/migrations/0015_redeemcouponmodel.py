# Generated by Django 3.1.4 on 2021-03-09 06:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupon', '0014_auto_20210306_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedeemCouponModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(default='', max_length=100, null=True)),
                ('coupon_code', models.CharField(default='', max_length=100, null=True)),
                ('green_point', models.CharField(default='', max_length=100, null=True)),
                ('coupon_redeem_date', models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 9, 12, 3, 52, 610732))),
                ('merchant_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 3.1.5 on 2021-02-18 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupon', '0008_auto_20210209_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='couponmodel',
            name='agegroup',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='category',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='ccode',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='cname',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='country',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='district',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='greenbill',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='state',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='vfrom',
        ),
        migrations.RemoveField(
            model_name='couponmodel',
            name='vthrough',
        ),
        migrations.AddField(
            model_name='couponmodel',
            name='coupon_code',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='couponmodel',
            name='coupon_name',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='couponmodel',
            name='coupon_value',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='couponmodel',
            name='green_point',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='couponmodel',
            name='merchant_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='couponmodel',
            name='valid_from',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='couponmodel',
            name='valid_through',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
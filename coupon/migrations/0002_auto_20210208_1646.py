# Generated by Django 3.1.6 on 2021-02-08 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponmodel',
            name='greenbill',
            field=models.BooleanField(verbose_name='My Green'),
        ),
        migrations.AlterField(
            model_name='couponmodel',
            name='mycustomer',
            field=models.BooleanField(verbose_name='customer'),
        ),
    ]

# Generated by Django 3.1.4 on 2021-03-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0012_couponmodel_coupon_background_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponmodel',
            name='coupon_user',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]

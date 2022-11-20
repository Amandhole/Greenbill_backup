# Generated by Django 3.1.4 on 2021-10-20 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0023_auto_20211020_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantbill',
            name='greenbill_digital_bill',
            field=models.BooleanField(blank=True, default=False, max_length=1000),
        ),
        migrations.AlterField(
            model_name='merchantbill',
            name='greenbill_sms_bill',
            field=models.BooleanField(blank=True, default=False, max_length=1000),
        ),
    ]

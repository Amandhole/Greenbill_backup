# Generated by Django 3.1.4 on 2021-11-17 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0035_auto_20211117_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savepetrolpumpbill',
            name='is_checkoutpin',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.1.4 on 2021-02-23 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0013_auto_20210223_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='savepetrolpumpbill',
            name='bill_flag',
            field=models.BooleanField(default=False),
        ),
    ]

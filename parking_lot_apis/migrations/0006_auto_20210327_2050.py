# Generated by Django 3.1.4 on 2021-03-27 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_apis', '0005_saveparkinglotbill_vehicle_type_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveparkinglotbill',
            name='reason',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='saveparkinglotbill',
            name='reason_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

# Generated by Django 3.1.4 on 2021-03-23 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_apis', '0004_auto_20210322_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveparkinglotbill',
            name='vehicle_type_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 3.1.4 on 2021-04-05 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_apis', '0010_saveparkinglotbill_pass_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinglotpass',
            name='vehicle_type',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='parkinglotpass',
            name='vehicle_type_id',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]

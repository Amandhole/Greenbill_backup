# Generated by Django 3.1.4 on 2021-03-19 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_apis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveparkinglotbill',
            name='flag_by',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

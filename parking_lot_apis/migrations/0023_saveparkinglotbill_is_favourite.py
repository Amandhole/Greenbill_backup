# Generated by Django 3.1.4 on 2021-09-27 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_apis', '0022_saveparkinglotbill_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveparkinglotbill',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
    ]

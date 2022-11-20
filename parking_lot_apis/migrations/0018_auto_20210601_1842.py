# Generated by Django 3.1.4 on 2021-06-01 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_apis', '0017_auto_20210514_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveparkinglotbill',
            name='reject_reason',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='saveparkinglotbill',
            name='reject_status',
            field=models.BooleanField(default=False),
        ),
    ]
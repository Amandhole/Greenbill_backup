# Generated by Django 3.1.4 on 2021-04-26 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_apis', '0014_saveparkinglotbill_green_points_earned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saveparkinglotbill',
            name='green_points_earned',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

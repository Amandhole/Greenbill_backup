# Generated by Django 3.1.4 on 2021-04-05 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_setting', '0026_compniesname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantparkinglotspace',
            name='entry_gate',
            field=models.BooleanField(blank=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='merchantparkinglotspace',
            name='vehicle_type',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
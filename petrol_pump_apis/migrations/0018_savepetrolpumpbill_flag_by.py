# Generated by Django 3.1.4 on 2021-03-19 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0017_savepetrolpumpbill_flag_update_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='savepetrolpumpbill',
            name='flag_by',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

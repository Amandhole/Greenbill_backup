# Generated by Django 3.1.4 on 2021-02-19 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0011_auto_20210219_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='savepetrolpumpbill',
            name='bill_tags',
            field=models.CharField(blank=True, default='', max_length=20000, null=True),
        ),
        migrations.AddField(
            model_name='savepetrolpumpbill',
            name='remarks',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]

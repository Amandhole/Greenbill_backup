# Generated by Django 3.1.4 on 2021-06-12 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0025_auto_20210601_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savepetrolpumpbill',
            name='bill_category_id',
            field=models.CharField(blank=True, default='26', max_length=100, null=True),
        ),
    ]

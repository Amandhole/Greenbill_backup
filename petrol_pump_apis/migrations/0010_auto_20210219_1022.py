# Generated by Django 3.1.4 on 2021-02-19 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0009_savepetrolpumpbill_bill_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savepetrolpumpbill',
            name='total_amount',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
    ]
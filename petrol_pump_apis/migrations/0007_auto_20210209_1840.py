# Generated by Django 3.1.4 on 2021-02-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0006_savepetrolpumpbill_worker_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='savepetrolpumpbill',
            name='bill_file',
            field=models.ImageField(blank=True, default='', null=True, upload_to='customer_bill'),
        ),
        migrations.AddField(
            model_name='savepetrolpumpbill',
            name='bill_url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='savepetrolpumpbill',
            name='c_unique_id',
            field=models.CharField(default='', max_length=20, null=True),
        ),
    ]

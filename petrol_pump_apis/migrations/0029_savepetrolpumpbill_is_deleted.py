# Generated by Django 3.1.4 on 2021-07-12 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0028_auto_20210619_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='savepetrolpumpbill',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]

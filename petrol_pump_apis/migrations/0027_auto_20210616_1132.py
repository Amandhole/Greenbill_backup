# Generated by Django 3.1.4 on 2021-06-16 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0026_auto_20210612_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='savepetrolpumpbill',
            name='p_business_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='savepetrolpumpbill',
            name='m_business_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

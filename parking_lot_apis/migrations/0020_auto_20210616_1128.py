# Generated by Django 3.1.4 on 2021-06-16 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot_apis', '0019_auto_20210612_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveparkinglotbill',
            name='p_business_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='saveparkinglotbill',
            name='m_business_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

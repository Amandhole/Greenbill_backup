# Generated by Django 3.1.4 on 2022-01-19 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0049_auto_20220119_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerbill',
            name='item_details',
            field=models.CharField(blank=True, default='', max_length=5000),
        ),
    ]

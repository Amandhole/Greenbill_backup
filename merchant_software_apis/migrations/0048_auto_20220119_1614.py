# Generated by Django 3.1.4 on 2022-01-19 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0047_auto_20220119_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerbill',
            name='item_details',
            field=models.CharField(default='', max_length=5000),
        ),
    ]

# Generated by Django 3.1.4 on 2021-10-29 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0028_auto_20211029_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='table_number',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]

# Generated by Django 3.1.4 on 2021-09-27 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0017_auto_20210910_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='merchantbill',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.1.4 on 2021-11-09 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner_stamp', '0003_merchantdeletedstamp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MerchantDeletedStamp',
        ),
        migrations.RemoveField(
            model_name='wstampmodels',
            name='is_check',
        ),
    ]
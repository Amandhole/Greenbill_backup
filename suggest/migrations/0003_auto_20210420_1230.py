# Generated by Django 3.1.4 on 2021-04-20 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suggest', '0002_ads_below_bill_created_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ads_below_bill',
            new_name='SuggestBusiness',
        ),
    ]

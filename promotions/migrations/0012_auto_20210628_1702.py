# Generated by Django 3.1.4 on 2021-06-28 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0011_auto_20210626_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads_below_bill',
            name='count',
            field=models.IntegerField(default='0', null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='count',
            field=models.IntegerField(default='0', null=True),
        ),
    ]

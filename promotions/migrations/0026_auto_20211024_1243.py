# Generated by Django 3.1.4 on 2021-10-24 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0025_auto_20211024_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads_below_bill',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

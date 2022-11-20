# Generated by Django 3.1.4 on 2022-01-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0046_auto_20220119_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='bill_discount',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='bill_gross_amount',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='customer_name',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='food_description',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='food_mrp',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]

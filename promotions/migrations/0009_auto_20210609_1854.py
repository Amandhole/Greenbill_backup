# Generated by Django 3.1.4 on 2021-06-09 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0008_bulkmailsmsmodel_receiver_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads_below_bill',
            name='ads_for',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_below_bill',
            name='days',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_below_bill',
            name='end_date',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_below_bill',
            name='merchant_business_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_below_bill',
            name='schedule',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='ads_below_bill',
            name='start_date',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='ads_for',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='ads_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='business_category_value',
            field=models.CharField(default='', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='business_name_value',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='days',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='end_date',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='merchants_name_value',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='schedule',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='start_date',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_merchants',
            name='ads_for',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_for_merchants',
            name='days',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]

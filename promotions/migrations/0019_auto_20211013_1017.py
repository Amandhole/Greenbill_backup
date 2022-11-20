# Generated by Django 3.1.4 on 2021-10-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0018_ads_below_bill_merchant_business_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads_below_bill',
            name='ads_image_four',
            field=models.FileField(blank=True, null=True, upload_to='ads_images'),
        ),
        migrations.AddField(
            model_name='ads_below_bill',
            name='ads_image_three',
            field=models.FileField(blank=True, null=True, upload_to='ads_images'),
        ),
        migrations.AddField(
            model_name='ads_below_bill',
            name='ads_image_two',
            field=models.FileField(blank=True, null=True, upload_to='ads_images'),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='ads_image_four',
            field=models.FileField(blank=True, null=True, upload_to='ads_images'),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='ads_image_three',
            field=models.FileField(blank=True, null=True, upload_to='ads_images'),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='ads_image_two',
            field=models.FileField(blank=True, null=True, upload_to='ads_images'),
        ),
    ]
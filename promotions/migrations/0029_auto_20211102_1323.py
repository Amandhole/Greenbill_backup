# Generated by Django 3.1.4 on 2021-11-02 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0028_promotionspaymenthistory_ads_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads_below_bill',
            name='clicks',
            field=models.IntegerField(default='0', null=True),
        ),
        migrations.AddField(
            model_name='ads_for_green_bills',
            name='clicks',
            field=models.IntegerField(default='0', null=True),
        ),
    ]
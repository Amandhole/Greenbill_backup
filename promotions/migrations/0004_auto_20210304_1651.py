# Generated by Django 3.1.4 on 2021-03-04 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0003_ads_for_merchants_business_category_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads_for_merchants',
            name='business_category_value',
            field=models.CharField(default='', max_length=2000, null=True),
        ),
    ]
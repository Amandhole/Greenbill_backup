# Generated by Django 3.1.4 on 2021-12-30 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_info', '0005_customer_info_model_merchant_business_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_info_model',
            name='customer_city',
            field=models.CharField(default='', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='customer_info_model',
            name='customer_state',
            field=models.CharField(default='', max_length=500, null=True),
        ),
    ]

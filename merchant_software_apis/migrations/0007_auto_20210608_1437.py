# Generated by Django 3.1.4 on 2021-06-08 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0006_auto_20210608_0147'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='green_bill_print_transaction',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='green_bill_transaction',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='print_transaction',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='merchantbill',
            name='green_bill_print_transaction',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='merchantbill',
            name='green_bill_transaction',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='merchantbill',
            name='print_transaction',
            field=models.BooleanField(default=False),
        ),
    ]

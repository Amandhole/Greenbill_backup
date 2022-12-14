# Generated by Django 3.1.4 on 2021-06-19 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0011_customerbill_partner_business_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='payment_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='payu_transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='merchantbill',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='merchantbill',
            name='payment_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='merchantbill',
            name='payu_transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='merchantbill',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

# Generated by Django 3.1.4 on 2021-11-16 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_sendpaymentmanually'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sendpaymentmanually',
            old_name='payment_for',
            new_name='bank_transaction_id',
        ),
        migrations.RenameField(
            model_name='sendpaymentmanually',
            old_name='payu_transaction_id',
            new_name='cheque_id',
        ),
        migrations.RenameField(
            model_name='sendpaymentmanually',
            old_name='transaction_id',
            new_name='description',
        ),
        migrations.AddField(
            model_name='sendpaymentmanually',
            name='payment_with',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

# Generated by Django 3.1.4 on 2021-06-12 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_ownerpaymentlinks_transcation_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownerpaymentlinks',
            name='payu_transaction_id',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]

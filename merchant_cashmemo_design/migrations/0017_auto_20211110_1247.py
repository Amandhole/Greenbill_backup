# Generated by Django 3.1.4 on 2021-11-10 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_cashmemo_design', '0016_auto_20210914_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercashmemodetailmodels',
            name='rejected_cash_memo',
            field=models.CharField(default='', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='customerreceiptdetailsmodels',
            name='rejected_receipt',
            field=models.CharField(default='', max_length=120, null=True),
        ),
    ]

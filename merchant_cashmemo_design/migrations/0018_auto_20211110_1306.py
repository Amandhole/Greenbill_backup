# Generated by Django 3.1.4 on 2021-11-10 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_cashmemo_design', '0017_auto_20211110_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customercashmemodetailmodels',
            name='rejected_cash_memo',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='customerreceiptdetailsmodels',
            name='rejected_receipt',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

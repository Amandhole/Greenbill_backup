# Generated by Django 3.1.4 on 2021-06-24 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_my_subscription', '0008_partner_recharge_history_invoice_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner_recharge_history',
            name='invoice_no',
            field=models.CharField(default='GB', max_length=120, null=True),
        ),
    ]

# Generated by Django 3.1.4 on 2021-06-25 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_subscription', '0020_auto_20210624_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recharge_history',
            old_name='bill_url',
            new_name='cheque_no',
        ),
        migrations.AddField(
            model_name='recharge_history',
            name='mode',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

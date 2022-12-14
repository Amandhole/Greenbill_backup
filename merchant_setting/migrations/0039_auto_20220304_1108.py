# Generated by Django 3.1.4 on 2022-03-04 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_setting', '0038_deleted_bills_by_days_setting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deleted_bills_by_days_setting',
            name='deleted_days',
        ),
        migrations.RemoveField(
            model_name='deleted_bills_by_days_setting',
            name='deleted_from',
        ),
        migrations.AddField(
            model_name='deleted_bills_by_days_setting',
            name='delete_days_customer',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AddField(
            model_name='deleted_bills_by_days_setting',
            name='delete_days_merchant',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AddField(
            model_name='deleted_bills_by_days_setting',
            name='delete_from_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='deleted_bills_by_days_setting',
            name='delete_from_merchant',
            field=models.BooleanField(default=False),
        ),
    ]

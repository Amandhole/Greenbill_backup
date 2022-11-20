# Generated by Django 3.1.4 on 2022-03-12 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_setting', '0040_deleted_bills_by_days_setting_date_entered'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantpaymentsetting',
            name='upi_id',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='merchantpaymentsetting',
            name='payu_key',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='merchantpaymentsetting',
            name='payu_salt',
            field=models.CharField(default=' ', max_length=200),
        ),
    ]
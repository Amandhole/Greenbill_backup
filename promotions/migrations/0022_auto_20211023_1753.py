# Generated by Django 3.1.4 on 2021-10-23 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0021_auto_20211013_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads_below_bill',
            name='approved_status',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='ads_below_bill',
            name='payment_done',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
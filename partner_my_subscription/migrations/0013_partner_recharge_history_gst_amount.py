# Generated by Django 3.1.4 on 2021-10-18 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_my_subscription', '0012_auto_20211005_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner_recharge_history',
            name='gst_amount',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
# Generated by Django 3.1.4 on 2021-02-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plan', '0006_auto_20210226_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='discount_amount',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

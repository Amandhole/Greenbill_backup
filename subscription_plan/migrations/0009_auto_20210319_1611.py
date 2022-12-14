# Generated by Django 3.1.4 on 2021-03-19 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plan', '0008_auto_20210319_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='digital_bill',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='digital_cashmemo_cost',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='discount_amount',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='discount_in_percentage',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='discount_in_value',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='per_bill_cost',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='sms_cashmemo_cost',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='software_maintainance',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='total_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

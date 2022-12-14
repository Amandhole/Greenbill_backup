# Generated by Django 3.1.4 on 2021-01-27 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plan', '0002_subscription_plan_details_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='addons',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='discount_in_percentage',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='discount_in_rupee',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='offered_cost',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='per_sms_cost',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='sms_count',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='sms_plan',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='sms_type',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='subscription_plan',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='total_cost',
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='digital_bill',
            field=models.FloatField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='ideal_for',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='min_recharge',
            field=models.FloatField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='per_bill_cost',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

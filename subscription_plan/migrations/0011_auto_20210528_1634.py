# Generated by Django 3.1.4 on 2021-05-28 11:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plan', '0010_auto_20210524_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='subscription_plan_details1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_name', models.CharField(blank=True, max_length=500, null=True)),
                ('per_bill_cost', models.CharField(blank=True, max_length=200, null=True)),
                ('digital_bill', models.CharField(blank=True, max_length=500, null=True)),
                ('min_recharge', models.CharField(default='', max_length=200, null=True)),
                ('ideal_for', models.CharField(blank=True, max_length=1000, null=True)),
                ('business_category', models.CharField(blank=True, default='', max_length=20000, null=True)),
                ('merchant_name', models.CharField(blank=True, default='', max_length=20000, null=True)),
                ('customized_plan_for', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('customized_plan', models.BooleanField(default=False, null=True)),
                ('is_active', models.BooleanField(default=False, null=True)),
                ('is_discount', models.BooleanField(default=False, null=True)),
                ('discount_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('discount_in_percentage', models.CharField(blank=True, max_length=100, null=True)),
                ('discount_in_value', models.CharField(blank=True, max_length=100, null=True)),
                ('sms_cashmemo_cost', models.CharField(max_length=100, null=True)),
                ('digital_cashmemo_cost', models.CharField(blank=True, max_length=100, null=True)),
                ('software_maintainance', models.CharField(blank=True, max_length=200, null=True)),
                ('total_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('plan_for', models.CharField(default='', max_length=500, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='subscription_plan_details',
            old_name='digital_cashmemo_cost',
            new_name='discount_in',
        ),
        migrations.RenameField(
            model_name='subscription_plan_details',
            old_name='discount_in_percentage',
            new_name='per_cash_memo_cost',
        ),
        migrations.RenameField(
            model_name='subscription_plan_details',
            old_name='discount_in_value',
            new_name='per_digital_bill_cost',
        ),
        migrations.RenameField(
            model_name='subscription_plan_details',
            old_name='total_amount',
            new_name='per_digital_cash_memo_cost',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='digital_bill',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='discount_amount',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='ideal_for',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='is_discount',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='min_recharge',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='plan_for',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='sms_cashmemo_cost',
        ),
        migrations.RemoveField(
            model_name='subscription_plan_details',
            name='software_maintainance',
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='per_digital_receipt_cost',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='per_receipt_cost',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='recharge_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='software_maintainace_cost',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='subscription_plan_cost',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='user_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan_details',
            name='valid_for_month',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subscription_plan_details',
            name='per_bill_cost',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 3.1.4 on 2021-05-28 17:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plan', '0014_auto_20210528_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotions_subscription_plan_model',
            name='is_discount',
        ),
        migrations.AddField(
            model_name='promotions_subscription_plan_model',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

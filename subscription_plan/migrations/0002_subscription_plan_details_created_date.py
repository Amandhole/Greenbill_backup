# Generated by Django 3.1.4 on 2021-01-23 17:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription_plan_details',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
# Generated by Django 3.1.4 on 2021-08-21 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plan', '0028_auto_20210820_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_on_plan_model',
            name='actual_final_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

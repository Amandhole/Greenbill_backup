# Generated by Django 3.1.4 on 2021-08-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plan', '0021_auto_20210712_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotional_subscription_plan_model',
            name='total_sms_avilable',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transactional_subscription_plan_model',
            name='total_sms_avilable',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]

# Generated by Django 3.1.4 on 2021-06-14 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner_my_subscription', '0006_auto_20210614_2141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partner_transactional_sms_subscriptions',
            old_name='merchant_id',
            new_name='partner_id',
        ),
        migrations.RemoveField(
            model_name='partner_transactional_sms_subscriptions',
            name='business_ids',
        ),
    ]

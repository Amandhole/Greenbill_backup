# Generated by Django 3.1.4 on 2021-08-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_info', '0006_bulkmailsmspartnermodel_sms_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulkmailsmspartnermodel',
            name='merchant_area',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='bulkmailsmspartnermodel',
            name='merchant_city',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='bulkmailsmspartnermodel',
            name='merchant_state',
            field=models.CharField(max_length=150, null=True),
        ),
    ]

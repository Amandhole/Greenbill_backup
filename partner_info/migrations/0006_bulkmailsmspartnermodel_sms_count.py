# Generated by Django 3.1.4 on 2021-08-08 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_info', '0005_auto_20210705_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulkmailsmspartnermodel',
            name='sms_count',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
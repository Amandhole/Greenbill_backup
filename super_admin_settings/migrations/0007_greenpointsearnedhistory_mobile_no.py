# Generated by Django 3.1.4 on 2021-06-05 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin_settings', '0006_greenpointsearnedhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='greenpointsearnedhistory',
            name='mobile_no',
            field=models.CharField(default=0, max_length=20, null=True),
        ),
    ]
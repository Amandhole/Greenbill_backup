# Generated by Django 3.1.4 on 2021-02-27 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_setting', '0010_merchantpetrolnozzle'),
    ]

    operations = [
        migrations.AddField(
            model_name='petrol_pump_app_setting_model',
            name='header_text1',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='petrol_pump_app_setting_model',
            name='header_text2',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='petrol_pump_app_setting_model',
            name='header_text3',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]

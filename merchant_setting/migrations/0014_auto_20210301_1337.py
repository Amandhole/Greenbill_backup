# Generated by Django 3.1.4 on 2021-03-01 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_setting', '0013_auto_20210227_1816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parking_app_setting_model',
            old_name='footer_text',
            new_name='footer_text1',
        ),
        migrations.AddField(
            model_name='parking_app_setting_model',
            name='footer_text2',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='parking_app_setting_model',
            name='footer_text3',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='parking_app_setting_model',
            name='header_text1',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='parking_app_setting_model',
            name='header_text2',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='parking_app_setting_model',
            name='header_text3',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]

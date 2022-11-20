# Generated by Django 3.1.4 on 2020-12-10 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='emailSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_type', models.CharField(max_length=100, null=True)),
                ('smtp_username', models.CharField(max_length=100, null=True)),
                ('smtp_password', models.CharField(max_length=100, null=True)),
                ('smtp_server', models.CharField(max_length=100, null=True)),
                ('smtp_port', models.CharField(max_length=100, null=True)),
                ('smtp_security', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='generalSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, null=True)),
                ('business_name', models.CharField(max_length=100, null=True)),
                ('business_code', models.CharField(max_length=50, null=True)),
                ('mobile_no', models.CharField(max_length=10, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('date_format', models.CharField(max_length=100, null=True)),
                ('currency', models.CharField(max_length=10, null=True)),
                ('android_app_url', models.CharField(max_length=100, null=True)),
                ('iphone_app_url', models.CharField(max_length=100, null=True)),
                ('o_business_logo', models.ImageField(blank=True, default='business_logos/business_logo.jpg', null=True, upload_to='business_logos')),
            ],
        ),
    ]
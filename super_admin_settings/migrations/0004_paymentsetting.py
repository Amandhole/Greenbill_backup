# Generated by Django 3.1.4 on 2020-12-30 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin_settings', '0003_sms_setting'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payu_key', models.CharField(max_length=100)),
                ('payu_salt', models.CharField(max_length=200)),
            ],
        ),
    ]

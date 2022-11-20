# Generated by Django 3.1.4 on 2020-12-30 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin_settings', '0002_auto_20201211_0801'),
    ]

    operations = [
        migrations.CreateModel(
            name='sms_setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('sender_id', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=0)),
            ],
        ),
    ]

# Generated by Django 3.1.4 on 2021-01-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210121_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant_users',
            name='m_business_id',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='merchant_users',
            name='raw_password',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]

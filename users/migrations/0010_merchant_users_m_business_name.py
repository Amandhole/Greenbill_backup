# Generated by Django 3.1.4 on 2021-01-25 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210123_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant_users',
            name='m_business_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]

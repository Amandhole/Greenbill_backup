# Generated by Django 3.1.4 on 2021-06-07 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0005_auto_20210608_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='rating',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='merchantbill',
            name='rating',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]

# Generated by Django 3.1.4 on 2021-05-18 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='is_customer',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='is_merchant',
            field=models.BooleanField(default=False),
        ),
    ]
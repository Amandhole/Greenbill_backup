# Generated by Django 3.1.4 on 2021-07-01 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_update', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='system_updates',
            name='group_parking',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='system_updates',
            name='group_petrol',
            field=models.BooleanField(default=False, null=True),
        ),
    ]

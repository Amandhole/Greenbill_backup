# Generated by Django 3.1.4 on 2021-07-03 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_update', '0003_unread_system_updates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unread_system_updates',
            name='notification_id',
            field=models.IntegerField(null=True),
        ),
    ]

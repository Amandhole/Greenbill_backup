# Generated by Django 3.1.4 on 2021-06-18 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20210617_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='greenbilluser',
            name='disable_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

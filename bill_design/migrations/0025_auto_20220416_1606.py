# Generated by Django 3.1.4 on 2022-04-16 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_design', '0024_auto_20220416_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact_card',
            name='sharecount',
        ),
        migrations.AddField(
            model_name='contact_card',
            name='share',
            field=models.IntegerField(default='0', null=True),
        ),
    ]
